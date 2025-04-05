// OrderManager.cpp
#include "OrderManager.h"
#include <cstdio>


Order::Order(int number, std::string asset, std::string type,
    std::string pair, double quantity, double price,
    std::string currency) {
    orderNumber = number;
    assetName = asset;
    assetType = type;
    assetPair = pair;
    orderQuantity = quantity;
    orderPrice = price;
    baseCurrency = currency;
}


OrderManager::OrderManager() {
    nextOrderNumber = 1;    // Start with order #1
    printf("OrderManager created\n");
}

OrderManager::~OrderManager() {
    printf("OrderManager destroyed\n");
}

void OrderManager::addOrder() {
    orderNumbers.push_back(nextOrderNumber);
    printf("Order #%d added\n", nextOrderNumber);
    nextOrderNumber++;
}