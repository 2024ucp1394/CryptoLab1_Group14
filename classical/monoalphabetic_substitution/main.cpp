#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <cctype>

using namespace std;

// --------------------------------------------------
// Encrypt using monoalphabetic substitution
// key[i] = ciphertext for plaintext 'a' + i
// --------------------------------------------------
string encryptText(string text, string key)
{
    string result = "";

    for (char ch : text)
    {
        if (isalpha(ch))
        {
            bool upper = isupper(ch);
            char x = tolower(ch);

            char encrypted = key[x - 'a'];

            if (upper)
                encrypted = toupper(encrypted);

            result += encrypted;
        }
        else
        {
            result += ch;
        }
    }

    return result;
}

// --------------------------------------------------
// 1. Frequency Analysis
// --------------------------------------------------
void frequency_analysis(string cipher)
{
    int freq[26] = {0};
    int total = 0;

    for (char ch : cipher)
    {
        if (isalpha(ch))
        {
            ch = tolower(ch);
            freq[ch - 'a']++;
            total++;
        }
    }

    vector<pair<char, int>> v;

    for (int i = 0; i < 26; i++)
    {
        if (freq[i] > 0)
            v.push_back({char('a' + i), freq[i]});
    }

    sort(v.begin(), v.end(),
         [](pair<char, int> a, pair<char, int> b)
         {
             return a.second > b.second;
         });

    cout << "\nLETTER FREQUENCY\n";
    cout << "----------------------------\n";

    for (auto p : v)
    {
        double percentage =
            (double)p.second * 100 / total;

        cout << p.first << " : "
             << p.second << " ("
             << percentage << "%)\n";
    }

    cout << "\nTotal letters = " << total << endl;
}

// --------------------------------------------------
// 2. Word Frequency Analysis
// --------------------------------------------------
void word_frequency_analysis(string cipher)
{
    map<string, int> freq;

    string word = "";

    for (char ch : cipher)
    {
        if (isalpha(ch))
        {
            word += tolower(ch);
        }
        else
        {
            if (!word.empty())
            {
                freq[word]++;
                word = "";
            }
        }
    }

    if (!word.empty())
        freq[word]++;

    vector<pair<string, int>> v;

    for (auto p : freq)
        v.push_back(p);

    sort(v.begin(), v.end(),
         [](pair<string, int> a, pair<string, int> b)
         {
             return a.second > b.second;
         });

    cout << "\nWORD FREQUENCY\n";
    cout << "----------------------------\n";

    int count = 0;

    for (auto p : v)
    {
        cout << p.first << " : "
             << p.second << endl;

        count++;

        if (count == 20)
            break;
    }
}

// --------------------------------------------------
// Generate pattern of a word
// Example: that -> 0120
// --------------------------------------------------
string getPattern(string word)
{
    map<char, int> number;
    int next = 0;

    string pattern = "";

    for (char ch : word)
    {
        if (number.find(ch) == number.end())
        {
            number[ch] = next++;
        }

        pattern += char('0' + number[ch]);
    }

    return pattern;
}

// --------------------------------------------------
// 3. Pattern Analysis
// --------------------------------------------------
void pattern_analysis(string cipher)
{
    map<string, int> patterns;
    string word = "";

    for (char ch : cipher)
    {
        if (isalpha(ch))
        {
            word += tolower(ch);
        }
        else
        {
            if (!word.empty())
            {
                if (word.length() >= 2)
                    patterns[getPattern(word)]++;

                word = "";
            }
        }
    }

    if (!word.empty() && word.length() >= 2)
        patterns[getPattern(word)]++;

    cout << "\nPATTERN ANALYSIS\n";
    cout << "----------------------------\n";

    for (auto p : patterns)
    {
        cout << "Pattern "
             << p.first
             << " : "
             << p.second
             << " words\n";
    }
}

// --------------------------------------------------
// 4. Apply substitution
// recoveredKey = ciphertext -> plaintext
// '?' means unknown
// --------------------------------------------------
string apply_substitution(string cipher,
                          string recoveredKey)
{
    string result = "";

    for (char ch : cipher)
    {
        if (isalpha(ch))
        {
            bool upper = isupper(ch);
            char x = tolower(ch);

            char plain = recoveredKey[x - 'a'];

            if (plain == '?')
                plain = '_';

            if (upper)
                plain = toupper(plain);

            result += plain;
        }
        else
        {
            result += ch;
        }
    }

    return result;
}

// --------------------------------------------------
// 5. Display Partial Plaintext
// --------------------------------------------------
void display_partial_plaintext(string cipher,
                               string key)
{
    cout << "\nPARTIAL PLAINTEXT\n";
    cout << "----------------------------\n";

    string result =
        apply_substitution(cipher, key);

    cout << result << endl;
}

// --------------------------------------------------
// 6. Verify Solution
// --------------------------------------------------
bool verify_solution(string plaintext,
                     string ciphertext,
                     string encryptionKey)
{
    string generated =
        encryptText(plaintext, encryptionKey);

    return generated == ciphertext;
}

// --------------------------------------------------
// MAIN
// --------------
int main(int argc, char *argv[])
{
    string filename;

    // If a testcase filename is given, use it.
    // Otherwise use plaintext.txt
    if (argc >= 2)
    {
        filename = argv[1];
    }
    else
    {
        filename = "plaintext.txt";
    }

    ifstream input(filename);

    if (!input)
    {
        cout << "Cannot open " << filename << "\n";
        return 1;
    }

    string plaintext = "";
    string line;

    while (getline(input, line))
    {
        plaintext += line;
        plaintext += '\n';
    }

    input.close();

    // Plaintext -> Ciphertext key
    string encryptionKey =
        "qazwsxedcrfvtgbyhnujmikolp";

    // Ciphertext -> Plaintext recovered key
    string recoveredKey =
        "boihgknqvtwyurxzajemsldfpc";

    // Encrypt
    string ciphertext =
        encryptText(plaintext, encryptionKey);

    cout << "\n========== CIPHERTEXT ==========\n";
    cout << ciphertext << endl;

    // Frequency analysis
    frequency_analysis(ciphertext);

    // Word frequency analysis
    word_frequency_analysis(ciphertext);

    // Pattern analysis
    pattern_analysis(ciphertext);

    // Partial plaintext
    display_partial_plaintext(ciphertext, recoveredKey);

    // Verification
    if (verify_solution(
            plaintext,
            ciphertext,
            encryptionKey))
    {
        cout << "\nVerification successful!\n";
        cout << "Recovered key is correct.\n";
    }
    else
    {
        cout << "\nVerification failed!\n";
    }

    return 0;
}
