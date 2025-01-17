const { ethers } = require("ethers");
const fs = require("fs");

async function main() {
    // Step 1: Connect to Ganache
    const provider = new ethers.providers.JsonRpcProvider("http://127.0.0.1:7545"); // Ganache RPC URL
    const signer = provider.getSigner(0); // Use the first Ganache account

    // Step 2: Load the Contract
    const contractAddress = "0x6b1E2f02a1E7D9a52eaE51a3694c6dD57C893eD8"; // Replace with your deployed contract address
    const abi = [
        "function recordTransaction(uint256,string,uint256,uint256,uint256,uint256,uint256,uint256,string,string,uint256) public",
        "function updateFraudStatus(uint256,string) public",
        "function getTransaction(uint256) public view returns (uint256,string,uint256,uint256,uint256,uint256,uint256,uint256,string,string,uint256,string,string)"
    ];
    const contract = new ethers.Contract(contractAddress, abi, signer);

    // Step 3: Read JSON File
    const data = readJsonFile("FraudData.json");

    console.log("Prepared transaction data:", data);

    // Step 4: Send Data to Contract
    const tx = await contract.recordTransaction(
        data.orderID,
        data.productCategory,
        Math.floor(data.quantityReturned),
        Math.floor(data.purchaseAmount),
        Math.floor(data.refundIssued),
        data.customerAccountAge,
        data.previousReturns,
        data.previousFraudReports,
        data.deliveryType,
        data.returnCondition,
        data.customerScore
    );

    console.log("Transaction sent. Hash:", tx.hash);

    // Step 5: Wait for Transaction Confirmation
    const receipt = await tx.wait();
    console.log("Transaction confirmed in block:", receipt.blockNumber);

    // Step 6: Retrieve Transaction from Blockchain
    const transaction = await getTransaction(contract, data.orderID);
console.log(transaction.processType);
    // Step 7: Call ML Model if Eligible
    if (transaction.processType === "Automatic Refund") {
        const mlResult = callMLModel(transaction);
        console.log("ML Model Result:", mlResult);

        // Step 8: Update Fraud Status in Blockchain
        const updateTx = await contract.updateFraudStatus(data.orderID, mlResult);
        const updateReceipt = await updateTx.wait();
        console.log("Fraud status updated in block:", updateReceipt.blockNumber);
    } else {
        console.log("Transaction requires manual processing. Skipping ML model.");
    }
}

// Helper functions
function readJsonFile(filePath) {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

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

function callMLModel(transaction) {
    const features = [
        transaction.quantityReturned,
        transaction.purchaseAmount,
        transaction.customerAccountAge,
        transaction.previousReturns,
        transaction.previousFraudReports
    ];
    // Dummy ML logic; replace with actual ML model inference
    const score = features.reduce((sum, feature) => sum + feature, 0);
    return score > 1000 ? "Fraud" : "Non-Fraud";
}

main().catch(console.error);
