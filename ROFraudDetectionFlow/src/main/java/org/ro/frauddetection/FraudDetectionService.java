package org.ro.frauddetection;

import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class FraudDetectionService {

    public static void handleLVR(OrderData order) {
        System.out.println(" LVR data-Fetching Customer Score ");

        int score = fetchCustomerScore(order.getCustomerId());
        System.out.println(" LVR data-Customer Score is: " + score);

        if (score < 50) {
            // Regular process and manual fraud analysis
            System.out.println(" LVR data- Customer Score < 50 , refund should be Manual ");

            updateRefundMode(order.getOrderId(), "Manual");
        } else {
            System.out.println(" LVR data- Customer Score > 50 , Performing Fraud Detection ");

            boolean isFraud = performFraudDetection(order);
            System.out.println(" LVR data- Fraud Detection status is Fraud : "+ isFraud);

            updateDatabaseAfterFraudCheck(order, isFraud);
        }
    }

    public static void handleNONLVR(OrderData order) {


        updateRefundMode(order.getOrderId(), "Manual");
    }

    public static int fetchCustomerScore(int customerId) {
        String query = "SELECT return_score FROM Customers WHERE customer_id = ?";
        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(query)) {
            pstmt.setInt(1, customerId);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("return_score");
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return -1; // Score not found
    }

    public static boolean performFraudDetection(OrderData order) {
        try (CloseableHttpClient client = HttpClients.createDefault()) {
            HttpPost httpPost = new HttpPost("http://localhost:5000/predict");

            // Create JSON payload using order data
            String json = createJsonPayload(order);
            StringEntity entity = new StringEntity(json);
            httpPost.setEntity(entity);
            httpPost.setHeader("Accept", "application/json");
            httpPost.setHeader("Content-type", "application/json");

            org.apache.http.HttpResponse response = client.execute(httpPost);
            String responseString = EntityUtils.toString(response.getEntity(), "UTF-8");
            return parseResponse(responseString);

        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    private static String createJsonPayload(OrderData order) {
        // Adapt this method to properly format your order data
        return String.format("{\"PurchaseAmount\": %.2f, \"ReturnCondition\": \"%s\"}",
                order.getProductPrice(),
                order.getReturnOrderStatus());
    }

    private static boolean parseResponse(String jsonResponse) {
        // Simple JSON parsing to extract fraud prediction
        return jsonResponse.contains("\"prediction\": \"Fraud\"");
    }

    public static void updateDatabaseAfterFraudCheck(OrderData order, boolean isFraud) {
        String condition = isFraud ? "fraud" : "non-fraud";
        String mode = isFraud ? "Fraud_Manual" : "AUTO";
        updateReturnOrderCondition(order.getOrderId(), condition);
        updateRefundMode(order.getOrderId(), mode);
        if (isFraud) {
            updateReturnScore(order.getCustomerId(), -10); // Deduct 10 points on fraud detection
        }
        System.out.println(" LVR data- Updated the Return Score (-10) and refund mode,Return Condition");

    }

    public static void updateReturnOrderCondition(int orderId, String condition) {
        String updateQuery = "UPDATE ReturnOrders SET return_order_condition = " +
                "? WHERE order_id = ?";
        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(updateQuery)) {
            pstmt.setString(1, condition);
            pstmt.setInt(2, orderId);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public static void updateRefundMode(int orderId, String mode) {
        System.out.println(" NON LVR data- Updated refund mode to Manual");

        String updateQuery = "UPDATE ReturnOrders SET refundmode = ?" +
                ", return_order_status =?" +
                " WHERE order_id = ?";
        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(updateQuery)) {
            pstmt.setString(1, mode);
            pstmt.setString(2, mode);
            pstmt.setInt(3, orderId);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public static void updateReturnScore(int customerId, int scoreAdjustment) {
        String updateQuery = "UPDATE Customers SET score = score + ? WHERE customer_id = ?";
        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(updateQuery)) {
            pstmt.setInt(1, scoreAdjustment);
            pstmt.setInt(2, customerId);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
