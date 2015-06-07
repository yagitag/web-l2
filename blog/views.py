from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import Http404

from blog.models import *

from datetime import datetime



def wrap_paginator(request, items, items_on_page_cnt = 5):
  paginator = Paginator(items, items_on_page_cnt)
  #
  try:
    page = int(request.GET.get("page", '1'))
  except ValueError:
    page = 1
  #
  try:
    items = paginator.page(page)
  except (InvalidPage, EmptyPage):
    items = paginator.page(paginator.num_pages)
  return items



def get_model_instacnce_by_id(model, model_instance_id):
  try:
    return model.objects.get(id=model_instance_id)
  except model.DoesNotExist:
    raise Http404




def get_posts(request):
  posts = Post.objects.all().order_by("-date")
  posts = wrap_paginator(request, posts)
  return render_to_response("list.html", dict(posts=posts), RequestContext(request))



def sign_up(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      new_user = form.save()
      return HttpResponseRedirect("/profile/")
  else:
    form = UserCreationForm()
  return render_to_response("registration/signup.html", { 'form' : form }, RequestContext(request))


@login_required
def get_profile(request):
  try:
    posts = Post.objects.filter(author=request.user.id).order_by("-date")
  except Post.DoesNotExist:
    posts = []
  posts = wrap_paginator(request, posts)
  return render_to_response("profile.html", dict(posts=posts), RequestContext(request))


def edit_post_fields(request, fields):
  (post_id, post) = load_post(request)
  #
  for field in fields:
    if not field in request.POST:
      return (post_id, post, '', True)
  #
  (post, errors) = update_post(request, post, fields)
  return (post_id, post, errors, False)


def update_post(request, post, fields):
  errors = ''
  for field in fields:
    value = request.POST[field]
    setattr(post, field, value)
    if not value:
      errors += 'Field "' + field + '" cannot be empty!\n'
  return (post, errors)


def load_post(request):
  post_id = request.GET.get('id', '')
  if post_id:
    #post = model.objects.get(id=post_id)
    post = get_model_instacnce_by_id(Post, post_id)
    if post.author != request.user:
      return HttpResponseRedirect("http://www.zakonrf.info/uk/137/")
  else:
    post = Post(author=request.user)
  return (post_id, post)


@login_required
def edit_post(request):
  if request.POST.get('cancel'):
    return HttpResponseRedirect("/profile/")
  #
  (post_id, post, errors, is_new) = edit_post_fields(request, ('title', 'content'))
  if errors or is_new:
    return render_to_response("edit.html", {'id':post_id,'post':post,'errors':errors}, RequestContext(request))
  else:
    try: idx = post.content.index('\n')
    except ValueError: idx = len(post.content)
    post.preview_char_cnt = idx + 1;
    post.save()
    return HttpResponseRedirect("/profile/")



def get_comment_child(comments_dict, comment, depth = 0):
  result = []
  if comment:
    comments_list = comments_dict[comment.id]
  else:
    comments_list = comments_dict[comment]
  for comment in comments_list:
    result.append(dict(id=comment.id, author=comment.author, content=comment.content, likes_cnt=comment.likes_cnt, date=comment.date, depth=depth))
    if comment.id in comments_dict:
      result.extend(get_comment_child(comments_dict, comment, depth + 1))
  return result



def convert_comments(comments):
  if not comments:
    return ({}, [])
  tmp_dict = {}
  for comment in comments:
    parent_id = comment.parent.id if comment.parent else None
    if parent_id in tmp_dict:
      tmp_dict[parent_id].append(comment)
    else:
      tmp_dict[parent_id] = [comment]
  #
  result = get_comment_child(tmp_dict, None)
  prev_depth = 0
  for item in result:
    cur_depth = item['depth']
    if cur_depth > prev_depth:
      item['inner_len'] = 'x' * (cur_depth - prev_depth)
    else:
      item['outer_len'] = 'x' * (prev_depth - cur_depth)
    prev_depth = cur_depth
  return (tmp_dict, result)



def handle_comments(request, post, max_depth):
  is_finished = False
  errors = ''
  comment_id = request.GET.get('comment_id', None)
  comment_parent_id = request.GET.get('comment_parent_id', None)
  if not comment_id:
    comment = Comment(author=request.user, post=post, parent_id=comment_parent_id)
  else:
    comment_id = int(comment_id)
    comment = get_model_instacnce_by_id(Comment, comment_id)
  #
  comment_content = request.POST.get('content', None)
  if comment_content and request.user.is_authenticated():
    is_finished = True
    comment.content = comment_content
    if int(request.GET.get('depth', 0)) < max_depth:
      comment.save()
    else:
      errors = 'Cannot insert new comment, cause max depth is ' + str(max_depth)
  #
  comments = Comment.objects.filter(post=post.id).order_by("date")
  (id_dict, comments) = convert_comments(comments)
  #
  (prev_comment_id, GET_str) = (None, '')
  if comment_id:
    GET_str = 'post_id={0}&comment_id={1}'.format(post.id, comment_id)
  elif comment_parent_id != None:
    if comment_parent_id:
      comment_parent_id = int(comment_parent_id)
    GET_str = 'post_id={0}&comment_parent_id={1}'.format(post.id, comment_parent_id)
  return (comments, comment_id, comment_parent_id, GET_str, is_finished, errors)



def show_post(request):
  MAX_DEPTH = 5
  post_id = request.GET.get('post_id', None)
  if not post_id:
    raise Http404
  #
  post = get_model_instacnce_by_id(Post, post_id)
  if request.POST.get('cancel'):
    return HttpResponseRedirect("/view/post?post_id=" + post_id)
  post = get_model_instacnce_by_id(Post, post_id)
  #
  (comments, comment_id, comment_parent_id, GET_str, is_finished, errors) = handle_comments(request, post, MAX_DEPTH)
  if is_finished:
    return HttpResponseRedirect("/view/post?post_id=" + post_id)
  #
  return render_to_response('post.html', {
    'id': post_id, 'post': post, 'comments': comments,
    'comment_id': comment_id, 'comment_parent_id': comment_parent_id,
    'GET_str': GET_str, 'errors': errors}, RequestContext(request))



def std_delete_model_instance(request, model):
  instance_id = request.GET.get('id', None)
  if not instance_id:
    raise Http404
  instance = get_model_instacnce_by_id(model, instance_id)
  instance.delete()



@login_required
def delete_post(request):
  std_delete_model_instance(request, Post)
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
def delete_comment(request):
  std_delete_model_instance(request, Comment)
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def like(request):
  creation_id = request.GET.get('id', None)
  str_is_positive = request.GET.get('is_positive', None)
  if creation_id and str_is_positive:
    creation = get_model_instacnce_by_id(UserCreation, creation_id)
    if creation.author != request.user.id:
      try:
        like = Like.objects.get(creation=creation, author=request.user)
        if not like.is_positive and str_is_positive == "yes":
          creation.likes_cnt += 2
          like.is_positive = True
        elif like.is_positive and str_is_positive == "no":
          creation.likes_cnt -= 2
          like.is_positive = False
      except:
        like = Like(creation=creation, author=request.user)
        if str_is_positive == "yes":
          creation.likes_cnt += 1
          like.is_positive = True
        else:
          creation.likes_cnt -= 1
          like.is_positive = False
      like.save()
      creation.save()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
