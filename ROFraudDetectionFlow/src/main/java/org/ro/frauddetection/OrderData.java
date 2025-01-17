package org.ro.frauddetection;

import lombok.Data;

@Data
public class OrderData {
    private int orderId;
    private int customerId;
    private double productPrice;
    private String returnOrderCondition;
    private String returnOrderStatus;

    // Default constructor
    public OrderData() {
        // Default constructor for Jackson deserialization
    }

    // Constructor with parameters
    public OrderData(int orderId, int customerId, double productPrice, String returnOrderCondition, String returnOrderStatus) {
        this.orderId = orderId;
        this.customerId = customerId;
        this.productPrice = productPrice;
        this.returnOrderCondition = returnOrderCondition;
        this.returnOrderStatus = returnOrderStatus;
    }

    // Getters and setters
    // Ensure to provide getters and setters for all fields

    // Override toString method for better logging
    @Override
    public String toString() {
        return "OrderData{" +
                "orderId=" + orderId +
                ", customerId=" + customerId +
                ", productPrice=" + productPrice +
                ", returnOrderCondition='" + returnOrderCondition + '\'' +
                ", returnOrderStatus='" + returnOrderStatus + '\'' +
                '}';
    }
}
