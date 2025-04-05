// OrderManager.h
#ifndef ORDER_MANAGER_H
#define ORDER_MANAGER_H

#include <vector>   
#include <string>




// Change to Builder Pattern later

struct OrderConfig {
    std::string assetName; // What is the asset called e.g. Bitcoin
    std::string assetType; // Asset Type, e.g. Crypto
    std::string assetPair; // i.e. USD/BTC
    double orderQuantity; // How many units ordered
    double orderPrice; // How much the order cost in base currency
    std::string baseCurrency; // Base currency for value, i.e.

    // Add a Constructor with default values


};




class Order {
// Keep attrtiubtes encaspliated within the boject only 
private:  
    int orderNumber; // Index for when it was ordered was ordered 
    OrderConfig config; // All order details store in confic struct
   
    

public:
    // Constructor decleration
    
    
    
    
  // Basic Getters
    int getOrderNumber() const { return orderNumber; }
    std::string getAssetName() const { return config.assetName; }
    std::string getAssetType() const { return config.assetType; }
    std::string getAssetPair() const { return config.assetPair; }
    double getQuantity() const { return config.orderQuantity; }
    double getOrderPrice() const { return config.orderPrice; }
    std::string getBaseCurrency() const { return config.baseCurrency; }
};



class OrderManager {
private:
    std::vector<int> orderNumbers;    // Just store order numbers for now
    int nextOrderNumber;              // Track the next order number

public:
    OrderManager();
    ~OrderManager();
    void addOrder();
};

#endif