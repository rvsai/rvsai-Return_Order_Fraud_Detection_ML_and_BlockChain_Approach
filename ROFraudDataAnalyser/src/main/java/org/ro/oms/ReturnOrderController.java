package org.ro.oms;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/return-orders")
public class ReturnOrderController {

    private final ReturnOrderService returnOrderService;

    @Autowired
    public ReturnOrderController(ReturnOrderService returnOrderService) {
        this.returnOrderService = returnOrderService;
    }

    @PostMapping
    public ReturnOrder addReturnOrder(@RequestBody ReturnOrder returnOrder) {
        return returnOrderService.addReturnOrder(returnOrder);
    }

    @GetMapping
    public List<ReturnOrder> getAllReturnOrders() {
        return returnOrderService.getAllReturnOrders();
    }
}
