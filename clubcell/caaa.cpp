#include<iostream>
using namespace std;

class income_tax{
    public:
        string pan_number;
        string name;
        int taxable_income;
        string address;
        int income_tax_amount;
    void enter_data(string pan, string name_of_person, int txbl_incm, string addrs){
        pan_number = pan;
        name= name_of_person;
        taxable_income= txbl_incm;
        address = addrs;
    }




};