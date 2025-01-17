package org.ro.frauddetection;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class OrderEventConsumer {

    private KafkaConsumer<String, String> consumer;
    private ObjectMapper objectMapper = new ObjectMapper();

    private FraudDetectionService fraudDetectionService=new FraudDetectionService();
    public OrderEventConsumer() {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "order-processing-group");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        
        consumer = new KafkaConsumer<>(props);
        consumer.subscribe(Collections.singletonList("returnOrdersTopic"));
    }

    public void processOrders() {
        while (true) {
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));
            for (ConsumerRecord<String, String> record : records) {
                processRecord(record.value());
            }
        }
    }

    private void processRecord(String orderData) {
        try {
            OrderData order = objectMapper.readValue(orderData, OrderData.class);
            System.out.println("Consumed message from  kafka"+ orderData);

       //     if (order.getReturnOrderCondition() == null || order.getReturnOrderCondition().isEmpty()) {
                if (order.getProductPrice() < 20) {
                    System.out.println(" LVR data ");

                    fraudDetectionService.handleLVR(order);
                } else {
                    System.out.println("NON_LVR data ");

                    fraudDetectionService.handleNONLVR(order);
                }
         //   }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public static void main(String[] args) {
        OrderEventConsumer consumer = new OrderEventConsumer();
        consumer.processOrders();
    }
}
