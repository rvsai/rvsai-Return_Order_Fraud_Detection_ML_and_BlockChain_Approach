package org.ro.oms;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ReturnOrderService {
    @Autowired
    private ReturnOrderRepository returnOrderRepository;

    public ReturnOrder addReturnOrder(ReturnOrder returnOrder) {
        returnOrder.setOrderId(3435L);
        return returnOrderRepository.save(returnOrder);
    }

    public List<ReturnOrder> getAllReturnOrders() {

        return returnOrderRepository.findAll();
    }
}
