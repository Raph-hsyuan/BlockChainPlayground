pragma solidity >=0.4.21 <0.7.0;

contract Adoption {
    address[16] public adopters;
    uint256 public counter = 0;
    function addCounter() public returns (uint256){
        return ++counter;
    }
    // Adopting a pet
    function adopt(uint256 petId) public returns (uint256) {
        require(petId >= 0 && petId <= 15, "petId not true");
        adopters[petId] = msg.sender;

        return petId;
    }
    // Retrieving the adopters
    function getAdopters() public view returns (address[16] memory) {
        return adopters;
    }
}
