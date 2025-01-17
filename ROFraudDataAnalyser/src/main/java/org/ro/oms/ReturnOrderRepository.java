package org.ro.oms;

import org.springframework.data.jpa.repository.JpaRepository;

public interface ReturnOrderRepository extends JpaRepository<ReturnOrder, Long> {
    // Add custom query methods if needed
}
