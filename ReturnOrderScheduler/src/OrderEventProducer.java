import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.ProducerConfig;
import java.util.Properties;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.sql.SQLException;
import java.util.Timer;
import java.util.TimerTask;

public class OrderEventProducer {
    private KafkaProducer<String, String> producer;
    private Connection connection;
    
    public OrderEventProducer() {
        // Initialize Kafka Producer
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer");
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer");
        producer = new KafkaProducer<>(props);
        
        // Initialize database connection
        try {
            connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/yourDatabaseName", "username", "password");
        } catch (SQLException e) {
            e.printStackTrace();
        }
        
        // Schedule the periodic task
        Timer timer = new Timer();
        timer.schedule(new FetchAndSendDataTask(), 0, 3600 * 1000);  // Schedule the task to run every hour
    }

    public void sendOrderData(String orderData) {
        producer.send(new ProducerRecord<>("returnOrdersTopic", orderData));
        producer.flush();
    }

    class FetchAndSendDataTask extends TimerTask {
        public void run() {
            try (Statement stmt = connection.createStatement()) {
                ResultSet rs = stmt.executeQuery("SELECT * FROM ReturnOrders WHERE return_order_condition IS NULL OR return_order_condition = ''");
                while (rs.next()) {
                    // Assuming the data from the ResultSet needs to be converted to a String format for Kafka
                    int orderId = rs.getInt("order_id");
                    double productPrice = rs.getDouble("product_price");
                    String orderData = "OrderID: " + orderId + ", Price: " + productPrice;
                    sendOrderData(orderData);
                }
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        new OrderEventProducer();
    }
}
