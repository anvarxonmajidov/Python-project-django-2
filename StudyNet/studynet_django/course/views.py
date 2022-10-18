from random import randint
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.text import slugify

from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes

from .models import Course,Lesson,Comment,Category
from .serializers import CourseListSerializer,CourseDetailSerializer,LessonListSerializer,CommentsSerializer,CategorySerializer,QuizSerializer, UserSerializer


@api_view(['POST'])
def create_course(request):

    status=request.data.get('status')

    print(request.data)

    if status=='published':
        status='draft'

    course=Course.objects.create(
        title=request.data.get('title'),
        slug='%s-%s'%(slugify(request.data.get('title')),randint(1000,10000)),
        short_description=request.data.get('short_description'),
        long_description=request.data.get('long_description'),
        status=status,
        created_by=request.user
    )
    for id in request.data.get('categories'):
        course.categories.add(id)
    course.save()

    # Lessons

    for lesson in request.data.get('lessons'):
        tmp_lesson=Lesson.objects.create(
            course=course,
            title=lesson.get('title'),
            slug=slugify(lesson.get('title')),
            short_description=lesson.get('short_description'),
            long_description=lesson.get('long_description'),
            status=Lesson.DRAFT
        )

    return Response({'course_id':course.id})

@api_view(['GET'])
def get_quiz(request,course_slug,lesson_slug):
    lesson=Lesson.objects.get(slug=lesson_slug)
    quiz=lesson.quizzes.first()
    serializer=QuizSerializer(quiz)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_categories(request):
    categories=Category.objects.all()
    serializer=CategorySerializer(categories,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_frontpage_courses(request):
    courses = Course.objects.filter(status=Course.PUBLISHED)[0:4]
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_courses(request):
    category_id=request.GET.get('category_id','')
    courses = Course.objects.filter(status=Course.PUBLISHED)

    if category_id:
        courses=courses.filter(categories__in=[int(category_id)])
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_course(request,slug):
    course=Course.objects.filter(status=Course.PUBLISHED).get(slug=slug)
    course_serializer=CourseDetailSerializer(course)
    lesson_serializer=LessonListSerializer(course.lessons.all(),many=True)
    
    if request.user.is_authenticated:
        course_data=course_serializer.data
    else:
        course_data={}

    return Response({
        'course':course_data,
        'lessons':lesson_serializer.data,
    })

@api_view(['GET'])
def get_comments(request,course_slug,lesson_slug):
    course=Course.objects.get(slug=course_slug)
    lesson=course.lessons.get(slug=lesson_slug)
    serializer=CommentsSerializer(lesson.comments.all(),many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_comment(request,course_slug,lesson_slug):
    data=request.data
    course=Course.objects.get(slug=course_slug)
    lesson=Lesson.objects.get(slug=lesson_slug)

    comment=Comment.objects.create(course=course,lesson=lesson,name=data.get('name'),content=data.get('content'),created_by=request.user)

    serializer=CommentsSerializer(comment)

    return Response(serializer.data)

@api_view(['GET'])
def get_author_courses(request,user_id):
    user=User.objects.get(pk=user_id)
    courses=user.courses.filter(status=Course.PUBLISHED)

    user_serializer=UserSerializer(user,many=False)
    courses_serializer=CourseListSerializer(courses,many=True)

    return Response({
        'courses':courses_serializer.data,
        'created_by':user_serializer.data
    })
"""
admin/
api/v1/ ^users/$ [name='user-list']
api/v1/ ^users\.(?P<format>[a-z0-9]+)/?$ [name='user-list']
api/v1/ ^users/activation/$ [name='user-activation']
api/v1/ ^users/activation\.(?P<format>[a-z0-9]+)/?$ [name='user-activation']
api/v1/ ^users/me/$ [name='user-me']
api/v1/ ^users/me\.(?P<format>[a-z0-9]+)/?$ [name='user-me']
api/v1/ ^users/resend_activation/$ [name='user-resend-activation']
api/v1/ ^users/resend_activation\.(?P<format>[a-z0-9]+)/?$ [name='user-resend-activation']
api/v1/ ^users/reset_password/$ [name='user-reset-password']
api/v1/ ^users/reset_password\.(?P<format>[a-z0-9]+)/?$ [name='user-reset-password']
api/v1/ ^users/reset_password_confirm/$ [name='user-reset-password-confirm']
api/v1/ ^users/reset_password_confirm\.(?P<format>[a-z0-9]+)/?$ [name='user-reset-password-confirm']
api/v1/ ^users/reset_username/$ [name='user-reset-username']
api/v1/ ^users/reset_username\.(?P<format>[a-z0-9]+)/?$ [name='user-reset-username']
api/v1/ ^users/reset_username_confirm/$ [name='user-reset-username-confirm']
api/v1/ ^users/reset_username_confirm\.(?P<format>[a-z0-9]+)/?$ [name='user-reset-username-confirm']
api/v1/ ^users/set_password/$ [name='user-set-password']
api/v1/ ^users/set_password\.(?P<format>[a-z0-9]+)/?$ [name='user-set-password']
api/v1/ ^users/set_username/$ [name='user-set-username']
api/v1/ ^users/set_username\.(?P<format>[a-z0-9]+)/?$ [name='user-set-username']
api/v1/ ^users/(?P<id>[^/.]+)/$ [name='user-detail']
api/v1/ ^users/(?P<id>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='user-detail']
api/v1/ ^$ [name='api-root']
api/v1/ ^\.(?P<format>[a-z0-9]+)/?$ [name='api-root']
api/v1/ ^token/login/?$ [name='login']
api/v1/ ^token/logout/?$ [name='logout']
api/v1/courses/
"""