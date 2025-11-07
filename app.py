from flask import Flask, render_template, redirect, url_for, flash, request
from config import DevelopmentConfig
from extensions import db, migrate, login_manager, csrf
from models import User, LeaveRequest
from forms import RegisterForm, LoginForm, LeaveForm, AdminActionForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf.csrf import generate_csrf
from forms import AdminActionForm

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ------ Auth routes ------
    @app.route('/')
    def index():
        return redirect(url_for('home'))
    @app.route('/home')
    def home():
        return render_template('home.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        form = RegisterForm()
        if form.validate_on_submit():
            existing = User.query.filter_by(email=form.email.data.lower()).first()
            if existing:
                flash('Email already registered', 'warning')
                return redirect(url_for('register'))
            is_admin = True if form.role.data == 'manager' else False
            user = User(
                email=form.email.data.lower(),
                name=form.name.data,
                password=generate_password_hash(form.password.data),
                is_admin=is_admin
            )
            db.session.add(user)
            db.session.commit()
            flash('Registered. Please log in.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        form = LoginForm()

        # Preserve the 'next' parameter (either from querystring or from POST)
        next_page = request.args.get('next') or request.form.get('next')

        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data.lower()).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Logged in successfully!', 'success')

                # Redirect to next if it's present and safe
                if next_page and is_safe_url(next_page):
                    return redirect(next_page)

                # Otherwise redirect based on role
                if user.is_admin:
                    return redirect(url_for('admin_dashboard'))
                return redirect(url_for('dashboard'))

            flash('Invalid credentials', 'danger')

        return render_template('login.html', form=form, next=next_page)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Logged out', 'info')
        return redirect(url_for('home'))

    # ------ Dashboard and leave routes ------
    # change this block: route now at '/dashboard' (not '/')
    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        leaves = LeaveRequest.query.filter_by(user_id=current_user.id).order_by(LeaveRequest.created_at.desc()).all()
        return render_template('dashboard.html', leaves=leaves)

    @app.route('/apply', methods=['GET', 'POST'])
    @login_required
    def apply_leave():
        form = LeaveForm()
        if form.validate_on_submit():
            lr = LeaveRequest(
                user_id=current_user.id,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                reason=form.reason.data,
                status='Pending'
            )
            db.session.add(lr)
            db.session.commit()
            flash('Leave applied', 'success')
            return redirect(url_for('dashboard'))
        return render_template('apply_leave.html', form=form)

    # ------ Admin routes ------
    @app.route('/admin')
    @login_required
    def admin_dashboard():
        if not current_user.is_admin:
            flash('Unauthorized', 'danger')
            return redirect(url_for('dashboard'))
        q = request.args.get('q')
        status = request.args.get('status')
        leaves = LeaveRequest.query
        if q:
            leaves = leaves.join(User).filter(User.name.ilike(f'%{q}%') | User.email.ilike(f'%{q}%'))
        if status:
            leaves = leaves.filter(LeaveRequest.status == status)
        leaves = leaves.order_by(LeaveRequest.created_at.desc()).all()
        #csrf_token = generate_csrf()
        form = AdminActionForm()
        return render_template('admin_dashboard.html', leaves=leaves,form=form)

    @app.route('/admin/action/<int:leave_id>', methods=['POST'])
    @login_required
    def admin_action(leave_id):
        if not current_user.is_admin:
            flash('Unauthorized', 'danger')
            return redirect(url_for('dashboard'))
        form = AdminActionForm()
        leave = LeaveRequest.query.get_or_404(leave_id)
        if form.validate_on_submit():
            if 'submit_approve' in request.form:
                leave.status = 'Approved'
                flash(f'Leave ID {leave_id} approved successfully!', 'success')
            elif 'submit_reject' in request.form:
                leave.status = 'Rejected'
                flash(f'Leave ID {leave_id} rejected.', 'warning')
            leave.admin_comment = form.admin_comment.data
            db.session.commit()
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid form submission.', 'danger')
            return redirect(url_for('admin_dashboard'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)