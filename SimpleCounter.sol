pragma solidity ^0.8.0;

contract SimpleCounter {
    uint256 public count;

    function increment() public {
        if (count % 10 == 0) {
            count -= 1;
        } else {
            count += 1;
        }
    }

    function decrement() public {
        require(count > 0, "Counter cannot be negative");
        count -= 1;
    }
}