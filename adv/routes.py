from flask import render_template, url_for, flash, redirect, request, abort
from adv import app, db, bcrypt, mail
from adv.forms import RegistrationForm, LoginForm, CreateGraphBarForm, CreateGraphNonBarForm, DeleteGraphForm, VideoForm, ContactForm, ScrapeForm
from adv.models import User, Video
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from adv.Data_Visualizer import create_bar



#from adv.data_viz_2 import create_bar1
class DataStore():
    """Classed used as a data storage as a means for transfering
    data between routes
    """
    video =  "<h1>No Video Created Yet!</h1>"#' <video width="320" height="240" controls> <source src="movi1e.mp4" type="video/mp4"> <source src="black.ogg" type="video/ogg"> Your browser does not support the video tag. </video>'


data = DataStore()

@app.route("/")
@app.route("/home")
def home():
    """renders home page
    """
    return render_template("layout.html", title="home")


@app.route("/register", methods=['GET', 'POST'])
def register():
    """Renders register page, and takes care of backend 
    operations such as saving information to database,
    hashing the password before saving it, confirming if
    password and confirm password match...etc
    """
    if current_user.is_authenticated:
        flash(f'You are already logged in!', 'danger')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You may login now!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Renders login page, and takes care of backend 
    operations such confirming if user has not already
    logged in and if the password is correct.
    """
    if current_user.is_authenticated:
        flash(f'You are already logged in!', 'danger')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    """Route to log out user
    """
    logout_user()
    return redirect(url_for('home'))

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    """route to users profile page, where the user's
    saved videos are located
    """
    videos = Video.query.filter_by(author = current_user).all()
    return render_template('profile.html', title='Profile', videos=videos, number = len(videos))

@app.route("/choose")
@login_required
def choose():
    """Renders page for choosing type of graph
    """
    return render_template('choose.html', title='choose')

@app.route("/create/<graph_type>", methods=['GET', 'POST'])
@login_required
def create(graph_type):
    """Renders page for creating a graph
    and creates a graph based on user choice

    :param graph_type: the type of graph
    :type graph_type: string
    """
    all_types = ['bar', 'line', 'scatter', 'pie']
    if graph_type not in all_types:
        abort(403)
    if graph_type == 'bar':
        form = CreateGraphBarForm()
    else:
        form = CreateGraphNonBarForm()
    if form.validate_on_submit():
        file = form.spreadsheet.data
        title = form.title.data
        if graph_type == 'bar':
            if form.sort.data == 'Ascending':
                sort_by = 'asc'
            else:
                sort_by = 'desc'
            bars = form.bars_visible.data
            if form.orientation.data == 'Horizontal':
                orien = 'h'
            else:
                orien = 'v'
            data.video = create_bar(file, graph_type, title, sort_by, bars, orien)
        else:
            data.video = create_bar(file, graph_type, title)
            """do this"""

        if not isinstance(data.video, str):
            data.video = data.video.data
        #data.video = create_bar(file, graph_type, 'hi')
        current_user.graphs_created += 1
        db.session.commit()
        flash(f'Your video has been created!', 'success')
        return redirect(url_for('video'))
    
    return render_template('creategraph.html', title='create', form = form, header=graph_type)

@app.route("/video", methods=['GET', 'POST'])
@login_required
def video():
    """page to render graphs video after being created.
    Saves video if user chooses to
    """
    form = VideoForm()
    if form.validate_on_submit():
        if len(data.video) == 30:
            flash(f'There is no video to save!', 'danger')
        else:
            if len(Video.query.filter_by(htmlcode=data.video).all()) > 0:
                flash(f'You have already saved this video!', 'danger')
            else:
                video = Video(author = current_user, htmlcode = data.video)
                db.session.add(video)
                db.session.commit()
                flash(f'Your video has been saved!', 'success')
        

    return render_template('video.html', title='video', form = form, header = data.video)

@app.route("/delete/<int:vid_id>", methods=['GET', 'POST'])
def delete(vid_id):
    """Page used to delete a specific video (specified by vid_id)

    :param vid_id: id of video to be deleted
    :type vid_id: int
    """
    form = DeleteGraphForm()
    video = Video.query.get_or_404(vid_id)
    if video.author != current_user:
        abort(403)
    if form.validate_on_submit():
        db.session.delete(video)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('delete.html', title='delete', form = form, video=video.htmlcode)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    """Page used to contact creators
    """
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message('Fan Mail From ' + form.name.data
            , sender = 'datavizassistance@gmail.com', recipients = ['datavizassistance@gmail.com'])
        msg.body = form.content.data + " From Email " + form.email.data
        mail.send(msg)
        flash('Message has been sent', 'success')
    return render_template('contact.html', title='Contact', form=form)


@app.route("/instructions")
def instructions():
    """Page containing Instructions on file format
    """
    return render_template('instructions.html', title='Instructions')

@app.route("/about")
def about():
    """About Page
    """
    return render_template('about.html', title='About Us')

@app.route("/scrape", methods=['GET', 'POST'])
def scrape():
    """Page that helps user web scrape data from other wesbites
    """
    form = ScrapeForm()
    if form.validate_on_submit():
        return redirect(url_for('download'))
    return render_template('scrape.html', title='Scrape Data', form = form)


@app.route("/download", methods=['GET', 'POST'])
def download():
    return render_template('download.html', title='Download')

