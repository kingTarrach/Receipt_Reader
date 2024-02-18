#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <regex>

using namespace std;

class Object 
{
    public:
        Object() : price(0) {}
        Object(string n, double p) : itemName(n), price(p) {}

        string itemName;
        double price;
};

int main()
{
    ifstream file;
    string line;
    vector<Object> items;

    file.open("text_result3.txt");

    if (!file.is_open()) {
        cout << "Error" << endl;
        return 1;
    }

    regex itemRegex(R"((.+?)\s+(\(\d+\)\s+)?(\d+\.\d+)\s*(?:x\s*(\d+))?)");
    double subtotal;

    while (getline(file, line)) {
        if (line.find("SUBTOTAL") != string::npos) {
            
            regex subtotalRegex(R"(\d+(?:[.,]\d+)?)");
            smatch subtotalMatch;
            if (regex_search(line, subtotalMatch, subtotalRegex)) {
                // Replace ',' with '.' for uniformity and then convert to double
                string subtotalStr = subtotalMatch[0];
                replace(subtotalStr.begin(), subtotalStr.end(), ',', '.');
                subtotal = stod(subtotalStr);
            }

            break; // Stop parsing when reaching the subtotal line
        }

        smatch match;
        if (regex_search(line, match, itemRegex)) {
            string itemName = match[1];
            double itemPrice = stod(match[3]);
            int itemQuantity = match[4].matched ? stoi(match[4]) : 1;

            items.push_back(Object{itemName, itemPrice});
        }
    }

    // Output the gathered information
    std::cout << "Items Purchased:" << endl;
    for (auto &i : items) {
        std::cout << i.itemName << " - $" << i.price << " x" << endl;
    }
    cout << "Subtotal: " << subtotal << endl;

    return 0;
}