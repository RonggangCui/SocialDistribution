from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import *
from .serializers import *
from .helpers import *
from .paginators import CustomPaginator
from rest_framework import status
from django.urls import reverse,resolve
from django.core.exceptions import *
from http import HTTPStatus

class AuthorListAPIView(APIView):
    def get(self, request):
        authors = Author.objects.all()
        paginator = CustomPaginator()
        result_page = paginator.paginate_queryset(authors, request)
        serializer = AuthorSerializer(result_page, many=True,context={'request':request,'kwargs':{}})

        data = {
            "type": "authors",
            "items": serializer.data
        }

        return Response(data)

class SingleAuthorAPIView(APIView):
    def get(self, request, author_id):
        author = Author.objects.get(id=author_id)

        serializer = AuthorSerializer(author, context={'request':request,'kwargs':{}})

        data = {
            "type": "author",
            "items": serializer.data
        }

        return Response(data)

    # In the requirements it says it should be POST. I kept it as put now, is that a typo on requirements since it says it should update the author
    def put(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response({"error": "Author does not exist"}, status=404)

        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

class AuthorFollowersAPIView(APIView):
    def get(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response({'error': 'Author does not exist'}, status=404)

        followers = author.followers.all()
        serializer = AuthorSerializer(followers, many=True, context={'request':request,'kwargs':{}})

        data = {
            "type": "followers",
            "items": serializer.data
        }

        return Response(data)




class FollowerAPIView(APIView):

    def get(self, request, author_id, follower_author_id):
            try:
                author = Author.objects.get(id=author_id)
                foreign_author = Author.objects.get(id=follower_author_id)
            except Author.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            is_following = foreign_author in author.followers.all()
            data = {
                "type": "followers",
                "is_following": is_following
            }
            return Response(data)

    #How to authenticate, do we need to set up like for example JWT tokens?
    def put(self, request, author_id, follower_author_id):
        try:
            author = Author.objects.get(id=author_id)
            foreign_author = Author.objects.get(id=follower_author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # # check if authenticated user is the author
        # if request.user != author:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        author.followers.add(foreign_author)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, author_id, follower_author_id):
        try:
            author = Author.objects.get(id=author_id)
            foreign_author = Author.objects.get(id=follower_author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # # check if authenticated user is the author
        # if request.user != author:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        if foreign_author in author.followers.all():
            author.followers.remove(foreign_author)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



class AuthorPostsView(APIView):
    def get(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        posts = Post.objects.filter(made_by=author).order_by('-date_published')


        paginator = CustomPaginator()
        result_page = paginator.paginate_queryset(posts, request)

        serializer = PostSerializer(result_page, many=True, context={'request':request,'kwargs':{'author_id':author_id}})
        return Response(serializer.data)

class PostDetailView(APIView):
    def get(self, request, author_id, post_id):
        try:
            post = Post.objects.get(uuid=post_id, visibility='PUBLIC')
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, context={'request':request,'kwargs':{'author_id':author_id,'post_id':post_id}})
        return Response(serializer.data)


    # Not sure how creating a post would look like (would the requester also send me the same json.)

    def post(self, request, author_id, post_id):
        try:
            post = Post.objects.get(uuid=post_id, made_by=request.user)
            return Response({"error": "Post with that id already exist"}, status=400)
        except Post.DoesNotExist:

            serializer = PostSerializer(post, data=request.data, context={'request':request,'kwargs':{'author_id':author_id,'post_id':post_id}})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, author_id, post_id):
        try:
            post = Post.objects.get(uuid=post_id, made_by=request.user)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, author_id, post_id):
        try:
            post = Post.objects.get(uuid=post_id, made_by=request.user)
        except Post.DoesNotExist:
            post = Post(uuid=post_id, made_by=request.user)

        serializer = PostSerializer(post,data=request.data, context={'request':request,'kwargs':{'author_id':author_id,'post_id':post_id}})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentsView(APIView):
    def get(self,request,author_id,post_id):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response({"error": "Author does not exist."}, status=400)
        try:
            post = Post.objects.get(uuid=post_id)
            comments = post.comments.all()
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist."}, status=400)

        paginator = CustomPaginator()
        result_page = paginator.paginate_queryset(comments, request)

        context = {'author_id':author_id,'post_id':post_id}
        serializer = CommentSerializer(result_page, many=True, context={'request':request,'kwargs':{'author_id':author_id,'post_id':post_id}})

        response = {
            "type": "Comments",
            "page": paginator.page.number,
            "size": paginator.get_page_size(request),
            "post": get_full_uri(request,'api-post-detail',context),
            "id": get_full_uri(request,'api-post-comments',context),
            "comments": serializer.data,
        }

        return Response(response)

    def post(self, request, author_id, post_id):
        user = Author.objects.get(id=get_values_from_uri(request.data.get('author').get('id'),add_api=True).get('author_id'))

        try:
            post = Post.objects.get(uuid=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist"}, status=400)
        serializer = CommentSerializer(data=request.data, context={'request':request,'post':post,'user':user,'kwargs':{'author_id':author_id,'post_id':post_id}})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikesPostView(APIView):
    def get(self,request,author_id,post_id):
        try:
            post = Post.objects.get(uuid=post_id)
            likes = post.likes.all()
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist."}, status=400)

        serializer = LikeSerializer(likes, many=True, context={'request':request,'kwargs':{'author_id':author_id,'post_id':post_id}})
        return Response(serializer.data)

    def post(self, request, author_id, post_id):
        user = Author.objects.get(id=get_values_from_uri(request.data.get('author').get('id'),add_api=True).get('author_id'))

        try:
            post = Post.objects.get(uuid=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist"}, status=400)
        if user == post.made_by:
            return Response({"error": "Can't like your own post"}, status=400)
        found = post.likes.filter(author=user)
        if found:
            return Response({"error": "Already liked post"}, status=400)
        serializer = LikeSerializer(data=request.data, context={'request':request,'user':user,'post':post,'kwargs':{'author_id':author_id,'post_id':post_id}})
        if serializer.is_valid():
            serializer.save()
            response = serializer.data
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikesCommentView(APIView):
    def get(self,request,author_id,post_id,comment_id):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response({"error": "Author does not exist."}, status=400)
        try:
            post = Post.objects.get(uuid=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist."}, status=400)
        try:
            comment = post.comments.get(uuid=comment_id)
            likes = comment.likes.all()
        except Comment.DoesNotExist:
            return Response({"error": "Comment does not exist."}, status=400)

        serializer = LikeSerializer(likes, many=True, context={'request':request,'kwargs':{'author_id':author_id,'post_id':post_id,'comment_id':comment_id}})
        return Response(serializer.data)

    def post(self, request, author_id, post_id, comment_id):
        user = Author.objects.get(id=get_values_from_uri(request.data.get('author').get('id'),add_api=True).get('author_id'))

        try:
            post = Post.objects.get(uuid=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist."}, status=400)
        try:
            comment = post.comments.get(uuid=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "Comment does not exist."}, status=400)
        if user == comment.author:
            return Response({"error": "Can't like your own comment"}, status=400)
        found = comment.likes.filter(author=user)
        if found:
            return Response({"error": "Already liked comment"}, status=400)
        serializer = LikeSerializer(data=request.data, context={'request':request,'user':user,'comment':comment,'kwargs':{'author_id':author_id,'post_id':post_id,'comment_id':comment_id}})
        if serializer.is_valid():
            serializer.save()
            response = serializer.data
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikedView(APIView):
    def get(self,request,author_id):
        try:
            author = Author.objects.get(id=author_id)
            liked = author.liked.all()
        except Author.DoesNotExist:
            return Response({"error": "Author does not exist."}, status=400)

        serializer = LikeSerializer(liked, many=True, context={'request':request,'kwargs':{'author_id':author_id}})

        response = {
            "type": "liked",
            "items": serializer.data,
        }

        return Response(response)
