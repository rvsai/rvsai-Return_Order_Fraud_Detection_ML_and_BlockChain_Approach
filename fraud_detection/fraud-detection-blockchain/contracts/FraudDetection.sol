// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract FraudDetection {
    struct Transaction {
        uint256 orderID;
        string productCategory;
        uint256 quantityReturned;
        uint256 purchaseAmount;
        uint256 refundIssued;
        uint256 customerAccountAge;
        uint256 previousReturns;
        uint256 previousFraudReports;
        string deliveryType;
        string returnCondition;
        uint256 customerScore;
        string fraudStatus; // ML Result: "Fraud" or "Non-Fraud"
        string processType; // Validation Result: "Automatic Refund" or "Manual Process"
    }

    mapping(uint256 => Transaction) public transactions;

    event TransactionRecorded(uint256 orderID, string processType, string fraudStatus);

    // Function to validate and record a transaction
    function recordTransaction(
        uint256 _orderID,
        string memory _productCategory,
        uint256 _quantityReturned,
        uint256 _purchaseAmount,
        uint256 _refundIssued,
        uint256 _customerAccountAge,
        uint256 _previousReturns,
        uint256 _previousFraudReports,
        string memory _deliveryType,
        string memory _returnCondition,
        uint256 _customerScore
    ) public {
        // Apply validation rules
        string memory processType = "Automatic Refund";

        if (_customerScore <= 70) {
            processType = "Manual Process";
        } else if (_purchaseAmount > 500) {
            processType = "Manual Process";
        } else if (
            keccak256(abi.encodePacked(_returnCondition)) ==
            keccak256(abi.encodePacked("Damaged")) ||
            keccak256(abi.encodePacked(_returnCondition)) ==
            keccak256(abi.encodePacked("Opened"))
        ) {
            processType = "Manual Process";
        } else if (_previousFraudReports > 2) {
            processType = "Manual Process";
        }

        // Record the transaction
        transactions[_orderID] = Transaction(
            _orderID,
            _productCategory,
            _quantityReturned,
            _purchaseAmount,
            _refundIssued,
            _customerAccountAge,
            _previousReturns,
            _previousFraudReports,
            _deliveryType,
            _returnCondition,
            _customerScore,
            "Pending", // Fraud status will be updated after ML model
            processType
        );

        emit TransactionRecorded(_orderID, processType, "Pending");
    }

    // Function to update fraud status after ML prediction
    function updateFraudStatus(uint256 _orderID, string memory _fraudStatus) public {
        require(bytes(transactions[_orderID].processType).length > 0, "Transaction does not exist");
        transactions[_orderID].fraudStatus = _fraudStatus;
    }

    // Function to retrieve a transaction
    function getTransaction(uint256 _orderID) public view returns (
        uint256, string memory, uint256, uint256, uint256, uint256, uint256, uint256, string memory, string memory, uint256, string memory, string memory
    ) {
        Transaction memory txn = transactions[_orderID];
        require(txn.orderID != 0, "Transaction does not exist");

        return (
            txn.orderID,
            txn.productCategory,
            txn.quantityReturned,
            txn.purchaseAmount,
            txn.refundIssued,
            txn.customerAccountAge,
            txn.previousReturns,
            txn.previousFraudReports,
            txn.deliveryType,
            txn.returnCondition,
            txn.customerScore,
            txn.fraudStatus,
            txn.processType
        );
    }
}
