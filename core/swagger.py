from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

UNAUTHORIZED = OpenApiResponse(
    description="Authentication required."
)

FORBIDDEN = OpenApiResponse(
    description="Permission denied."
)

NOT_FOUND = OpenApiResponse(
    description="Resource not found."
)

VALIDATION_ERROR = OpenApiResponse(
    description="Validation error."
)

def list_docs(
        *,
        tag,
        serializer,
        description
):

    return extend_schema(

        tags=[tag],

        summary=f"List {tag.lower()}",

        description=description,

        responses={
            200: serializer(many=True),
            401: UNAUTHORIZED,
            403: FORBIDDEN,
        }
    )

def create_docs(
        *,
        tag,
        request_serializer,
        response_serializer,
        description,
):

    return extend_schema(

        tags=[tag],

        summary=f"Create {tag[:-1].lower()}",

        description=description,

        request=request_serializer,

        responses={
            201: response_serializer,
            400: VALIDATION_ERROR,
            401: UNAUTHORIZED,
            403: FORBIDDEN,
        },
    )

def detail_docs(
        *,
        tag,
        serializer,
        description,
):

    return extend_schema(

        tags=[tag],

        summary=f"Retrieve {tag[:-1].lower()}",

        description=description,

        responses={
            200: serializer,
            404: NOT_FOUND,
        },
    )

def update_docs(
        *,
        tag,
        request_serializer,
        response_serializer,
        description,
):

    return extend_schema(

        tags=[tag],

        summary=f"Update {tag[:-1].lower()}",

        description=description,

        request=request_serializer,

        responses={
            200: response_serializer,
            400: VALIDATION_ERROR,
            404: NOT_FOUND,
        },
    )

def delete_docs(
        *,
        tag,
        description,
):

    return extend_schema(

        tags=[tag],

        summary=f"Delete {tag[:-1].lower()}",

        description=description,

        responses={
            200: OpenApiResponse(
                description="Deleted successfully."
            ),

            404: NOT_FOUND,
        },
    )

def restore_docs(
        *,
        tag,
        serializer,
        description,
):

    return extend_schema(

        tags=[tag],

        summary=f"Restore {tag[:-1].lower()}",

        description=description,

        responses={
            200: serializer,
            404: NOT_FOUND,
        },
    )


def statistics_docs(
        *,
        tag,
        serializer,
        description,
):

    return extend_schema(

        tags=[tag],

        summary=f"{tag} statistics",

        description=description,

        responses={
            200: serializer,
        },
    )