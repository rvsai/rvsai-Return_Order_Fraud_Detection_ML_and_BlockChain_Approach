const hre = require("hardhat");

async function main() {
    const FraudDetection = await hre.ethers.getContractFactory("FraudDetection");
    const fraudDetection = await FraudDetection.deploy();
    await fraudDetection.deployed();

    console.log(`FraudDetection deployed to: ${fraudDetection.address}`);
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
