from flask import Blueprint, request, render_template, redirect
from flask_login import login_required, current_user
from datetime import datetime
from app.posts.forms import PostForm, CommentForm
from app.models import PostsModel, User, Comment
from app.tools.check_auth import check_auth
from app.tools.save_file import save_file
from app.tools.nav_link_list import generate_nav_links

posts_blueprint = Blueprint('posts',
                            __name__,
                            template_folder='templates'
                            )


# server:port/blueprint_prefix/add
@posts_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def list_posts():
    """
    shows all posts and lets signed-in users post a picture, text or both
    """
    form_post = PostForm()
    form_comment = CommentForm()
    all_posts = PostsModel.query.all()
    all_comments = Comment.query.all()
    authors = User

    if request.method == 'POST' and check_auth():
        if form_comment.validate_on_submit():
            text = form_comment.comment_text.data
            post_id = form_comment.post_id.data
            time = datetime.now()
            Comment.add(time, text, current_user.id, post_id)

        elif form_post.validate_on_submit():
            if form_post.post_text.data or form_post.media.data:
                text = form_post.post_text.data
                media = form_post.media.data
                time = datetime.now()

                if media:
                    media = save_file(current_user.username, media, 'post_uploads')  # saves file to directory, returns filename

                PostsModel.add(time, text, media, current_user.id)

        return redirect('/posts')

    else:
        return render_template('posts.html', pages=generate_nav_links(), form_post=form_post, form_comment=form_comment, all_posts=all_posts, authors=authors, all_comments=all_comments)
