from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from .serializers import RevisionSerializer
from .models import Revision

class RevisionViewSet(viewsets.ReadOnlyModelViewSet):

    """ViewSet for displaying revisions. """
    queryset = Revision.objects.all()
    serializer_class = RevisionSerializer
    filter_fields = ('model', 'ref_model', 'target_id', 'ref_id')
    ordering_fields = ('created_at',)
    ordering = ('-created_at', )

    @detail_route(methods=['post'])
    def revert(self, request, *args, **kwargs):
        revision = self.get_object()
        if revision.revert():
            user = {'name': request.user.username, 'email': request.user.email}
            Revision.objects.create(
                action='revert',
                model=revision.model,
                target_id=revision.target_id,
                target_name=revision.target_name,
                ref_model=revision.ref_model,
                ref_id=revision.ref_id,
                snapshot=revision.snapshot,
                user=user)
            serializer = self.serializer_class(revision)
            return Response(serializer.data)
        return Response({'detail': 'Revert failed'}, status=status.HTTP_400_BAD_REQUEST)
