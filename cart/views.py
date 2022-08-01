from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from cart.models import Cart
from book.models import Book
from user.models import User
from cart.serializers import CartSerializer, GetCartSerializer, EditCartSerializer
from user.authentication import verify_token
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class CartAPIView(GenericAPIView):
    serializer_class = CartSerializer

    @swagger_auto_schema(request_body=CartSerializer)
    @verify_token
    def post(self, request):
        try:

            if not request.user.is_verified:
                return Response({'success': False,
                                 'message': "Only verified user can perform this action"},
                                status=status.HTTP_404_NOT_FOUND)
            new_book = request.data
            cart_id = new_book.get('id')
            # print(cart_id)
            user = User.objects.get(id=request.user.pk)
            # print(user)
            book = Book.objects.get(id=new_book.get('book_id'))
            # print(book)
            if not book:
                return Response({'success': False,
                                 'message': "Book is not found with this id",
                                 'data': book.id}, status=status.HTTP_404_NOT_FOUND)
            total_amt = book.price * new_book.get('quantity')
            if new_book.get('quantity') > book.quantity_now:
                return Response({'success': False,
                                 'message': "The given quantity is not available",
                                 'data': f"Only this much is available:- {book.quantity_now}"},
                                status=status.HTTP_404_NOT_FOUND)

            cart = Cart.objects.create(
                id=cart_id,
                user_id=user,
                book_id=book,
                quantity=new_book.get('quantity'),
                price_per_item=book.price,
                total_price=total_amt
            )
            cart.save()
            return Response({'success': True,
                             'message': "Successfully added in cart"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False,
                             'message': "Something went wrong",
                             'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # @swagger_auto_schema(request_body=GetCartSerializer)
    @verify_token
    def get(self, request):
        try:
            if not request.user.is_verified:
                return Response({'success': False,
                                 'message': "Only verified user can perform this action"},
                                status=status.HTTP_404_NOT_FOUND)
            user = User.objects.get(id=request.user.pk)
            if not user:
                return Response({'success': False,
                                 'message': "Not able to find that user"}, status=status.HTTP_404_NOT_FOUND)
            cart = Cart.objects.filter(user_id=user)
            serializer = GetCartSerializer(instance=cart, many=True)
            return Response({'success': True,
                             'message': "Cart Items",
                             'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False,
                             'message': "Something went wrong",
                             'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request, id):
        try:
            if not request.user.is_verified:
                return Response({'success': False,
                                 'message': "Only verified user can perform this action"},
                                status=status.HTTP_404_NOT_FOUND)
            cart = Cart.objects.get(id=id)
            print(cart.user_id)
            cart.delete()
            return Response({'success': True,
                             'message': "Successfully deleted "}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False,
                             'message': "Something went wrong",
                             'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=EditCartSerializer)
    @verify_token
    def patch(self, request, id):
        try:
            if not request.user.is_verified:
                return Response({'success': False,
                                 'message': "Only verified user can perform this action"},
                                status=status.HTTP_404_NOT_FOUND)
            data = request.data
            serializer = EditCartSerializer(data=data)
            if serializer.is_valid():
                quantity = serializer.data['quantity']
                cart = Cart.objects.get(id=id)
                if not cart:
                    return Response({'success': False,
                                     'message': "Given cart item is not Available",
                                     'data': id},
                                    status=status.HTTP_404_NOT_FOUND)
                cart.quantity = quantity
                cart.total_price = cart.book_id.price * quantity
                cart.save()
                return Response({'success': True,
                                 'message': "Successfully Edited the cart item "}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False,
                             'message': "Something went wrong",
                             'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)

