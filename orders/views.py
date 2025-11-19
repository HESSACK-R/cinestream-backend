# cinestream/backend/orders/views.py
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer, OrderItemSerializer, PaymentSerializer
from telegram_bot.bot import notify_admin

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().order_by("-created_at")
        return Order.objects.filter(user=user).order_by("-created_at")

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        total = order.total_price
        user = self.request.user

        # Notify admin after order creation
        try:
            msg_admin = (
                f"🛍️ *Nouvelle commande reçue !*\n\n"
                f"👤 Client : {user.username}\n"
                f"📱 Telegram : {user.telegram_number or 'Non fourni'}\n"
                f"💰 Total : {total} FCFA\n"
                f"🧾 Commande n°{order.id}\n"
                f"📅 Date : {order.created_at.strftime('%d/%m/%Y %H:%M')}"
            )
            notify_admin(msg_admin)
     
        except Exception as e:
            print(f"⚠️ Erreur notification Telegram lors de la création de commande : {e}")


@api_view(['DELETE'])
def delete_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.delete()
        return Response({"message": "Commande supprimée avec succès!"}, status=status.HTTP_204_NO_CONTENT)
    except Order.DoesNotExist:
        return Response({"error": "Commande non trouvée."}, status=status.HTTP_404_NOT_FOUND)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__user=user)

    def perform_create(self, serializer):
        user = self.request.user
        order = Order.objects.filter(user=user).order_by("-created_at").first()
        serializer.save(order=order)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by("-created_at")
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all().order_by("-created_at")
        return Payment.objects.filter(order__user=user).order_by("-created_at")

    def perform_create(self, serializer):
        print("📸 === DEBUG PAYMENT UPLOAD ===")
        print("FILES:", self.request.FILES)
        print("DATA:", self.request.data)
        
        user = self.request.user
        order_id = self.request.data.get("order")
        
        # Récupère la commande spécifique, sinon None
        order = Order.objects.filter(id=order_id, user=user).first()
        if not order:
            raise serializers.ValidationError({"error": "Commande introuvable ou non autorisée."})

        payment = serializer.save(
            order=order,
            screenshot=self.request.FILES.get("screenshot")  
        )
    
        print("=== Uploaded file ===", self.request.FILES.get("screenshot"))

        # ✅ Met à jour le statut
        order.status = "PAID"
        order.save(update_fields=["status"])

        # 🔔 Notifications Telegram
        try:
            msg_admin = (
                f"💰 *Nouveau paiement reçu !*\n\n"
                f"👤 Client : {user.username}\n"
                f"💳 Méthode : {payment.method}\n"
                f"🧾 Commande n°{order.id}\n"
                f"📅 Date : {payment.created_at.strftime('%d/%m/%Y %H:%M')}"
            )
            notify_admin(msg_admin)

        except Exception as e:
            print(f"⚠️ Erreur notification Telegram lors du paiement : {e}")