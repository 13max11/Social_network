from django.shortcuts import render, get_object_or_404, redirect
from .models import Community, Community_folow, Community_rule, CommunityGroup , Post, Comment, Like, DisLike, PostView, CommunityView
from .forms import PostCreationForm, CommunityCreationForm
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils import timezone
from django.utils.timezone import now, timedelta
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    posts = Post.objects.all()
    communitys = Community.objects.all()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        query = request.GET.get('q', '').strip()
        filtered_communities = Community.objects.filter(name__icontains=query) if query else []
        
        data = [{'id': c.id, 'name': c.name, 'slug': c.slug} for c in filtered_communities]
        return JsonResponse({'communities': data})

    context = {
        'posts': posts,
        'communitys':communitys,
    }
    return render(request,'index.html', context)

def community_details_view(request, slug):
    community = get_object_or_404(Community, slug=slug)
    rules = Community_rule.objects.filter(community=community)
    posts = Post.objects.filter(community=community)
    followers = community.community_follow.count()
    joined = None
    if request.user.is_authenticated:
        joined = Community_folow.objects.filter(community=community, user=request.user).first()


    context = {
        'community':community,
        'rules':rules,
        'posts':posts,
        'followers':followers,
        'joined':joined,
    }

    if request.user.is_authenticated:
            CommunityView.objects.update_or_create(
                user=request.user,
                community=community,
                defaults={'viewed_at': timezone.now()}
            )

    if request.method == 'POST' and request.user.is_authenticated:
        if "join" in request.POST:
                if request.user.is_authenticated:
                    if joined:
                        joined.delete()
                    else:
                        Community_folow.objects.create(community=community, user=request.user)
                    return redirect('community', slug=slug)
        
    return render(request, 'forum/community_details.html', context)

def post_details_view(request, slug, pk):
    community = Community.objects.get(slug=slug)
    post = get_object_or_404(Post, community=community, pk=pk)
    comments = Comment.objects.filter(post=post)
    likes = post.likes.count()
    dislikes = post.dislikes.count()
    liked = disliked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(post=post, user=request.user).first()
        disliked = DisLike.objects.filter(post=post, user=request.user).first()
    reputation = likes - dislikes

    if request.user.is_authenticated:
            PostView.objects.update_or_create(
                user=request.user,
                post=post,
                defaults={'viewed_at': timezone.now()}
            )

    if request.method == 'POST' and request.user.is_authenticated:
        if "comment" in request.POST:
            content = request.POST.get("content", "").strip()
            if content:
                Comment.objects.create(
                    post=post,
                    content=content,
                    user=request.user
                )
                messages.success(request, "Comment added successfully.")
                return redirect('post', slug=slug, pk=pk)
            else:
                messages.error(request, "Comment cannot be empty.")
        if "like" in request.POST:
            if request.user.is_authenticated:
                if disliked:
                    disliked.delete()
                if liked:
                    liked.delete()
                else:
                    Like.objects.create(post=post, user=request.user)
                return redirect('post', slug=slug, pk=pk)
            else:
                return redirect('login')
        if "dislike" in request.POST:
            if request.user.is_authenticated:
                if liked:
                    liked.delete()
                if disliked:
                    disliked.delete()
                else:
                    DisLike.objects.create(post=post, user=request.user)
                return redirect('post', slug=slug, pk=pk)
            else:
                return redirect('login')
    

    context = {
        'post': post,
        'comments': comments,
        'reputation':reputation,
        'liked':liked,
    }
    return render(request, 'forum/post_details.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect('post',post.community.slug, post.pk)
    else:
        form = PostCreationForm()

    return render(request, 'forum/create_post.html', {'form': form})

@login_required
def community_create(request):
    if request.method == 'POST':
        form = CommunityCreationForm(request.POST, request.FILES)
        if form.is_valid():
            community = form.save(commit=False)
            community.created_by = request.user
            community.save()
            return redirect('community', community.slug)
    else:
        form = CommunityCreationForm()

    return render(request, 'forum/create_community.html', {'form': form})

def explore(request):
    week_ago = now() - timedelta(days=7)

    random_communitys = Community.objects.all().order_by('?')

    # Сортування за кількістю підписників
    communitys_by_followers = Community.objects.annotate(
        followers_count=Count('community_follow')
    ).order_by('-followers_count')

    # Сортування за кількістю постів за останній тиждень
    communitys_by_posts = Community.objects.annotate(
        weekly_posts=Count('post', filter=Q(post__created_at__gte=week_ago))
    ).order_by('-weekly_posts')

    context = {
        'random_communitys':random_communitys,
        'communitys_by_followers': communitys_by_followers,
        'communitys_by_posts': communitys_by_posts,
    }

    return render(request, 'forum/explore.html', context)