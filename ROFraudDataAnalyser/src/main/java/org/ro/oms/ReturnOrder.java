package org.ro.oms;


import javax.persistence.*;

@Entity
@Table(name = "returnorders") // Specify the table name here
public class ReturnOrder {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "order_id")
    private Long orderId;
    private Long customerId;
    private Double productPrice;
    private String returnOrderCondition;
    private String returnOrderStatus;


    public Long getOrderId() {
        return orderId;
    }

    public void setOrderId(Long orderId) {
        this.orderId = orderId;
    }

    public Long getCustomerId() {
        return customerId;
    }

    public void setCustomerId(Long customerId) {
        this.customerId = customerId;
    }

    public Double getProductPrice() {
        return productPrice;
    }

    public void setProductPrice(Double productPrice) {
        this.productPrice = productPrice;
    }

    public String getReturnOrderCondition() {
        return returnOrderCondition;
    }

    public void setReturnOrderCondition(String returnOrderCondition) {
        this.returnOrderCondition = returnOrderCondition;
    }

    public String getReturnOrderStatus() {
        return returnOrderStatus;
    }

    public void setReturnOrderStatus(String returnOrderStatus) {
        this.returnOrderStatus = returnOrderStatus;
    }
}
