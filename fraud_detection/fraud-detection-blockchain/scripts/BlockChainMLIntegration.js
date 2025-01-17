const { ethers } = require("ethers");
const fs = require("fs");
const axios = require("axios");

async function main() {
    // Step 1: Connect to Ganache
    const provider = new ethers.providers.JsonRpcProvider("http://127.0.0.1:7545");
    const signer = provider.getSigner(0); // Use the first Ganache account

    // Step 2: Load the Contract
    const contractAddress = "0x0de3029CE25e113B5020449bbe653031b25BcCf8"; // Replace with your deployed contract address
    const abi = [
        "function recordTransaction(uint256,string,uint256,uint256,uint256,uint256,uint256,uint256,string,string,uint256) public",
        "function getTransaction(uint256) public view returns (uint256,string,uint256,uint256,uint256,uint256,uint256,uint256,string,string,uint256,string,string)",
        "function updateFraudStatus(uint256,string) public"
    ];
    const contract = new ethers.Contract(contractAddress, abi, signer);

    // Step 3: Read JSON Transactions
    const transactions = JSON.parse(fs.readFileSync("ROtransactions.json", "utf8"));

    // Initialize metrics
    let totalTransactions = 0;
    let truePositives = 0;
    let trueNegatives = 0;
    let falsePositives = 0;
    let falseNegatives = 0;
    let totalGasUsed = 0;

    for (const data of transactions) {
        try {
            

            totalTransactions++;

            const groundTruth = data.Fraud; // Use Fraud directly from JSON
            console.log(`Processing Transaction ID: ${data.orderID}`);

            // Step 4: Send transaction to the blockchain
            const tx = await contract.recordTransaction(
                data.orderID,
                data.productCategory,
                Math.round(data.quantityReturned), // Round to nearest integer
                Math.round(data.purchaseAmount), // Round to nearest integer
                Math.round(data.refundIssued), // Round to nearest integer
                data.customerAccountAge,
                data.previousReturns,
                data.previousFraudReports,
                data.deliveryType,
                data.returnCondition,
                data.customerScore
            );

            const receipt = await tx.wait();
            totalGasUsed += receipt.gasUsed.toNumber();

            // Step 5: Retrieve transaction from the blockchain
            const blockchainTransaction = await getTransaction(contract, data.orderID);

            let mlResult = "";
            if (blockchainTransaction.processType === "Automatic Refund") {
                // Step 6: Call ML Model API
                mlResult = await callPredictAPI(data);
                console.log("ML Model Result:", mlResult);

                // Step 7: Update Fraud Status in Blockchain
                const updateTx = await contract.updateFraudStatus(data.orderID, mlResult);
                const updateReceipt = await updateTx.wait();
                console.log(`Fraud status updated in block: ${updateReceipt.blockNumber}`);
            } else {
                console.log("Transaction requires manual processing. Skipping ML model.");
				mlResult='Fraud';
            }

            // Step 8: Compare blockchain validation and prediction with ground truth
            const predictedFraud = mlResult === "Fraud" ? 1 : 0;

            if (predictedFraud === 1 && groundTruth === 1) {
                truePositives++;
            } else if (predictedFraud === 0 && groundTruth === 0) {
                trueNegatives++;
            } else if (predictedFraud === 1 && groundTruth === 0) {
                falsePositives++;
            } else if (predictedFraud === 0 && groundTruth === 1) {
                falseNegatives++;
            }
        } catch (error) {
            console.error(`Error processing transaction ${data.orderID}:`, error);
        }
    }

    // Step 9: Calculate metrics
    const precision = truePositives / (truePositives + falsePositives || 1);
    const recall = truePositives / (truePositives + falseNegatives || 1);
    const f1Score = 2 * (precision * recall) / (precision + recall || 1);
    const validationAccuracy = (truePositives + trueNegatives) / totalTransactions;

    console.log("\n--- Metrics ---");
    console.log(`Total Transactions: ${totalTransactions}`);
    console.log(`Validation Accuracy: ${(validationAccuracy * 100).toFixed(2)}%`);
    console.log(`Precision: ${(precision * 100).toFixed(2)}%`);
    console.log(`Recall: ${(recall * 100).toFixed(2)}%`);
    console.log(`F1-Score: ${(f1Score * 100).toFixed(2)}%`);
    console.log(`False Positives: ${falsePositives}`);
    console.log(`False Negatives: ${falseNegatives}`);
    console.log(`Total Gas Used: ${totalGasUsed}`);
}

// Function to retrieve a transaction from the blockchain
async function getTransaction(contract, orderID) {
    const transaction = await contract.getTransaction(orderID);
    return {
        orderID: transaction[0].toNumber(),
        productCategory: transaction[1],
        quantityReturned: transaction[2].toNumber(),
        purchaseAmount: transaction[3].toNumber(),
        refundIssued: transaction[4].toNumber(),
        customerAccountAge: transaction[5].toNumber(),
        previousReturns: transaction[6].toNumber(),
        previousFraudReports: transaction[7].toNumber(),
        deliveryType: transaction[8],
        returnCondition: transaction[9],
        customerScore: transaction[10].toNumber(),
        fraudStatus: transaction[11],
        processType: transaction[12]
    };
}

// Function to call the ML model API
async function callPredictAPI(data) {
    const apiURL = "http://127.0.0.1:5000/predict";
    const payload = {
        QuantityReturned: data.quantityReturned,
        PurchaseAmount: data.purchaseAmount,
        CustomerAccountAge: data.customerAccountAge,
        PreviousReturns: data.previousReturns,
        PreviousFraudReports: data.previousFraudReports,
        RefundIssued: data.refundIssued,
        ProductCategory: data.productCategory,
        ReasonForReturn: data.ReasonForReturn,
        DeliveryType: data.deliveryType,
        ReturnCondition: data.returnCondition
    };

    try {
        const response = await axios.post(apiURL, payload);
        return response.data.prediction;
    } catch (error) {
        console.error("Error calling ML model API:", error);
        return "Error";
    }
}

main().catch(console.error);
