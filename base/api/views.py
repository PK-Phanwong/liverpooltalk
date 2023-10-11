from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Content
from .serializers import ContentSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/contents',
        'GET /api/contents/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getContents(request):
    contents = Content.objects.all()
    serializer = ContentSerializer(contents, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getContent(request, pk):
    content = Content.objects.get(id=pk)
    serializer = ContentSerializer(content, many=False)
    return Response(serializer.data)