from django.contrib import admin
from django.core.exceptions import PermissionDenied

from blog.models import Post, UserProfile, Comment, BlockedUser


# Register your models here.

class CommentAdmin(admin.StackedInline):
    model = Comment
    extra = 1
    list_display = ["comment_content", "date_written"]

    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        if obj and (request.user == obj.author.user or request.user == obj.post.author.user):
            if request.user.is_superuser:
                return True
        return False

    def has_change_permission(self, request, obj=None):
        if obj and (request.user == obj.author.user or request.user == obj.post.author.user):
            return True
        return False


# admin.site.register(Comment, CommentAdmin)


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentAdmin]
    list_display = ("title", "author",)
    list_filter = ("date_created",)
    search_fields = ("title", "content",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            blocked = BlockedUser.objects.filter(blockedu=request.user).values_list("blocker", flat=True)
            qs = qs.exclude(author__user__in=blocked)
        return qs

    def has_view_permission(self, request, obj=None):
        return True

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.author.user != request.user:
            return self.readonly_fields + ['title', 'content']
        return self.readonly_fields

    def has_change_permission(self, request, obj=None):
        if obj and obj.author.user != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj and obj.author.user != request.user:
            return False
        if request.user.is_superuser:
            return True
        return True


admin.site.register(Post, PostAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.user != request.user:
            return self.readonly_fields + ('user',)
        return self.readonly_fields


#  def has_view_permission(self, request, obj=None):
#     return True

#  def has_delete_permission(self, request, obj=None):
#     return obj is not None and request.user == obj.user

#  def has_change_permission(self, request, obj=None):
#   return obj is not None and request.user == obj.user

# def has_add_permission(self, request):
#    return request.user.is_superuser


admin.site.register(UserProfile, UserProfileAdmin)
