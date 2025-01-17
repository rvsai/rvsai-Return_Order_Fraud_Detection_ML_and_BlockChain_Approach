require("@nomiclabs/hardhat-ethers");


module.exports = {
    solidity: {
        version: "0.8.28",
        settings: {
            optimizer: {
                enabled: true,
                runs: 200,
            },
            viaIR: true, // Enable Intermediate Representation
        },
    },
networks: {
    localhost: {
      url: "http://127.0.0.1:7545", // Ganache RPC server
      accounts: [
        "0x99fa95bb6ce440a0f8ae7d17b7574694f9865664d44d9d6509d597c4e4ce2e2c"
		], // Replace with private keys from Ganache
    },
  },
};
