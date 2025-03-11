from .models import Community, CommunityView, CommunityGroup

def global_context(request):
    if request.user.is_authenticated:
        return {
                'followed_communitys': Community.objects.filter(community_follow__user=request.user),
                'recent_communitys': CommunityView.objects.filter(user=request.user).order_by('-viewed_at')[:5],
                'community_groups': CommunityGroup.objects.filter(creator=request.user),

        }
    else:
        return {
                '[]':[]
        }