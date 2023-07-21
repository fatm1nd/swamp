// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract Leaves is ERC20{

    address private _mintor;
    uint256 private fee_coeff_to_service = 7;

    constructor(address mintor) ERC20("Leaves","LVS"){
        _mintor = mintor;
    }

    function getFeeCoeff() public view returns (uint256){
        return fee_coeff_to_service;
    }

    function transferToMany(address[] memory users, uint256 amountPerUser) public{
        require((users.length) * amountPerUser <= balanceOf(msg.sender),"Not have enough money");

        uint8 l = uint8(users.length);

        for(uint i = 0; i < l; i++){
            _transfer(msg.sender, users[i], amountPerUser);
        }
    }

    function buyPaperNFT(address addressOfPaperNFT, uint256 token_id, uint8 level) public{
        PaperNFT paperContract = PaperNFT(addressOfPaperNFT);
        bool isPaperBought = paperContract.isPaperBought(token_id);
        require(!isPaperBought,"paper is already bought");
        PaperNFT.Request memory r = paperContract.getRequest(token_id);
        require(r.reader == msg.sender,"Paper is not yours");

        uint256 fee = r.ai_level_cost_request * fee_coeff_to_service; // fee to service is coeff multiple cost for one ai post

        if (level == 0){
            require((r.ai_level_cost_request + fee) <= balanceOf(msg.sender));
            transferToMany(r.ai_authors, r.ai_level_cost_request);
            _transfer(msg.sender, _mintor, fee);
            paperContract.changeLevel(token_id,0);
        }
        else {
            if (level == 1){
                require((r.begginers_level_cost_request + r.ai_level_cost_request + fee) <= balanceOf(msg.sender));
                transferToMany(r.ai_authors, r.ai_level_cost_request);
                transferToMany(r.begginers_authors, r.begginers_level_cost_request);
                _transfer(msg.sender, _mintor, fee);
                paperContract.changeLevel(token_id,1);
            }
            else{
                if (level == 2){
                    require((r.begginers_level_cost_request + r.ai_level_cost_request + r.middle_level_cost_request  + fee) <= balanceOf(msg.sender));
                    transferToMany(r.ai_authors, r.ai_level_cost_request);
                    transferToMany(r.begginers_authors, r.begginers_level_cost_request);
                    transferToMany(r.middle_authors, r.middle_level_cost_request);
                    _transfer(msg.sender, _mintor, fee);
                    paperContract.changeLevel(token_id,2);
                }
                else{
                    if (level == 3){
                        require((r.begginers_level_cost_request + r.ai_level_cost_request + r.middle_level_cost_request + r.pros_level_cost_request + fee) <= balanceOf(msg.sender));
                        transferToMany(r.ai_authors, r.ai_level_cost_request);
                        transferToMany(r.begginers_authors, r.begginers_level_cost_request);
                        transferToMany(r.middle_authors, r.middle_level_cost_request);
                        transferToMany(r.pros_authors, r.pros_level_cost_request);
                        _transfer(msg.sender, _mintor, fee);
                        paperContract.changeLevel(token_id,3);
                    }
                    else{
                        return;
                    }
                }
            }
        }
        //Transfer Paper to User
        paperContract.transferFrom(_mintor, msg.sender,token_id);
    }

    function mintTokenForUser(address reader, uint256 amount) public{
        require(msg.sender == _mintor,"You are not main server");
        _mint(reader, amount);
    }

    function burnTokenFromUser(address reader, uint256 amount) public{
        require(msg.sender == _mintor,"You are not main server");
        _burn(reader,amount);
    }

}



contract PaperNFT is ERC721{

    address private _mintor; 

    uint256 private tokenCounter = 1;

    uint128 private _unit_cost;

    struct Request{
        uint256 token_id;

        address reader;

        string sign_message;

        uint128 ai_level_cost_request;
        address[] ai_authors;

        uint128 begginers_level_cost_request;
        address[] begginers_authors;

        uint128 middle_level_cost_request;
        address[] middle_authors;

        uint128 pros_level_cost_request;
        address[] pros_authors;

        int8 boughtLevel; 
    }



    mapping(uint256 token_id => Request) private _requests;

    constructor(address mintor, uint128 unit_cost) ERC721("Paper","PPR"){
        _mintor = mintor;
        _unit_cost = unit_cost;
    }

    function getRequest(uint256 token_id) public view returns (Request memory){
        return _requests[token_id];
    }

    function setRequest(uint256 token_id, string memory sign_message, address reader, address[] memory ai_authors, address[] memory begginers_authors,address[] memory middle_authors, address[] memory pros_authors) public {
        require(msg.sender == _mintor);
        _requests[token_id] = Request(token_id, reader, sign_message,
        (_unit_cost ), ai_authors,
        (_unit_cost * 2), begginers_authors,
        (_unit_cost * 3), middle_authors,
        (_unit_cost * 4), pros_authors,
        -1
        );
    }

    function changeLevel(uint256 token_id, int8 level) public{
        require(level < 4 && level >= 0);
        require(tx.origin == _requests[token_id].reader);
        _requests[token_id].boughtLevel = level;
    }

    function isPaperBought(uint256 token_id) public view returns (bool){
        _requireMinted(token_id);
        return ownerOf(token_id) != _mintor;
    }

    function _safeMint(address to, uint256 tokenId) override internal virtual {
        _safeMint(to, tokenId, "");
    }

    function createNewPaper(string memory sign_message, address reader, address[] memory ai_authors, address[] memory begginers_authors,address[] memory middle_authors, address[] memory pros_authors, address leavesOperator) public returns (uint256){
        require(msg.sender == _mintor);
        _safeMint(_mintor,tokenCounter);
        setRequest(tokenCounter, sign_message, reader, ai_authors, begginers_authors, middle_authors, pros_authors);
        _setApprovalForAll(_mintor, leavesOperator, true);
        tokenCounter += 1;
        return tokenCounter - 1;
    
    }

}

