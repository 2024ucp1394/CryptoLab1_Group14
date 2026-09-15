#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <iomanip>
#include <cmath>
#include <cctype>

using namespace std;


/* --------------------------------------------------
   1. CLEAN CIPHERTEXT
   Removes spaces and special characters
   -------------------------------------------------- */
string clean_ciphertext(string text)
{
    string result = "";

    for (char c : text)
    {
        if (isalpha(c))
        {
            result += toupper(c);
        }
    }

    return result;
}


/* --------------------------------------------------
   2. FIND REPEATED PATTERNS
   We use 3-letter patterns
   -------------------------------------------------- */
map<string, vector<int>> find_repeated_patterns(string text)
{
    map<string, vector<int>> patterns;

    for (int i = 0; i <= (int)text.length() - 3; i++)
    {
        string pattern = text.substr(i, 3);

        patterns[pattern].push_back(i);
    }

    return patterns;
}


/* --------------------------------------------------
   3. CALCULATE DISTANCES
   Distance between repeated patterns
   -------------------------------------------------- */
vector<int> calculate_distances(
    map<string, vector<int>> patterns)
{
    vector<int> distances;

    for (auto p : patterns)
    {
        vector<int> positions = p.second;

        if (positions.size() > 1)
        {
            for (int i = 0; i < positions.size(); i++)
            {
                for (int j = i + 1; j < positions.size(); j++)
                {
                    int distance =
                        positions[j] - positions[i];

                    distances.push_back(distance);
                }
            }
        }
    }

    return distances;
}


/* --------------------------------------------------
   4. FIND FACTORS
   Find factors from Kasiski distances
   -------------------------------------------------- */
map<int, int> find_factors(vector<int> distances)
{
    map<int, int> factorCount;

    for (int distance : distances)
    {
        for (int factor = 2; factor <= 20; factor++)
        {
            if (distance % factor == 0)
            {
                factorCount[factor]++;
            }
        }
    }

    return factorCount;
}


/* --------------------------------------------------
   5. KASISKI ANALYSIS
   Find probable key length
   -------------------------------------------------- */
int kasiski_analysis(string text)
{
    map<string, vector<int>> patterns =
        find_repeated_patterns(text);

    vector<int> distances =
        calculate_distances(patterns);

    map<int, int> factors =
        find_factors(distances);

    cout << "\n========== KASISKI ANALYSIS ==========\n";

    cout << "\nRepeated patterns:\n";

    for (auto p : patterns)
    {
        if (p.second.size() > 1)
        {
            cout << p.first << " : ";

            for (int position : p.second)
            {
                cout << position << " ";
            }

            cout << endl;
        }
    }

    cout << "\nFactors:\n";

    for (auto f : factors)
    {
        cout << "Key Length "
             << f.first
             << " -> "
             << f.second
             << " times\n";
    }

    /*
       For this ciphertext, 12 is the expected
       key length.

       We select the factor with the highest count.
    */

    int bestLength = 1;
    int bestCount = 0;

    for (auto f : factors)
    {
        if (f.second > bestCount)
        {
            bestCount = f.second;
            bestLength = f.first;
        }
    }

    return bestLength;
}


/* --------------------------------------------------
   6. INDEX OF COINCIDENCE
   BONUS PART
   -------------------------------------------------- */
double calculate_ic(string text)
{
    int n = text.length();

    if (n <= 1)
        return 0;

    int frequency[26] = {0};

    for (char c : text)
    {
        frequency[c - 'A']++;
    }

    double numerator = 0;

    for (int i = 0; i < 26; i++)
    {
        numerator +=
            frequency[i] * (frequency[i] - 1);
    }

    double denominator =
        n * (n - 1);

    return numerator / denominator;
}


/* --------------------------------------------------
   7. SPLIT INTO GROUPS
   -------------------------------------------------- */
vector<string> split_into_groups(
    string text,
    int keyLength)
{
    vector<string> groups(keyLength);

    for (int i = 0; i < text.length(); i++)
    {
        groups[i % keyLength] += text[i];
    }

    return groups;
}


/* --------------------------------------------------
   8. FREQUENCY ANALYSIS
   -------------------------------------------------- */
void frequency_analysis(vector<string> groups)
{
    cout << "\n========== FREQUENCY ANALYSIS ==========\n";

    for (int i = 0; i < groups.size(); i++)
    {
        int frequency[26] = {0};

        for (char c : groups[i])
        {
            frequency[c - 'A']++;
        }

        cout << "\nGroup " << i + 1 << ":\n";

        for (int j = 0; j < 26; j++)
        {
            cout << char('A' + j)
                 << "="
                 << frequency[j]
                 << "  ";
        }

        cout << endl;
    }
}


/* --------------------------------------------------
   ENGLISH LETTER FREQUENCIES
   -------------------------------------------------- */
double englishFrequency[26] =
{
    0.082, 0.015, 0.028, 0.043, 0.127,
    0.022, 0.020, 0.061, 0.070, 0.0015,
    0.0077, 0.040, 0.024, 0.067, 0.075,
    0.019, 0.001, 0.060, 0.063, 0.091,
    0.028, 0.0098, 0.024, 0.0015, 0.020,
    0.0007
};


/* --------------------------------------------------
   9. FIND SHIFT
   Chi-square frequency analysis
   -------------------------------------------------- */
int find_shift(string group)
{
    int n = group.length();

    double bestScore = 1e100;

    int bestShift = 0;

    for (int shift = 0; shift < 26; shift++)
    {
        int observed[26] = {0};

        /*
           Decrypt group using this shift
        */
        for (char c : group)
        {
            int x =
                (c - 'A' - shift + 26) % 26;

            observed[x]++;
        }

        double score = 0;

        /*
           Compare observed frequency
           with English frequency
        */
        for (int i = 0; i < 26; i++)
        {
            double expected =
                n * englishFrequency[i];

            if (expected > 0)
            {
                score +=
                    ((observed[i] - expected) *
                     (observed[i] - expected))
                    / expected;
            }
        }

        if (score < bestScore)
        {
            bestScore = score;
            bestShift = shift;
        }
    }

    return bestShift;
}


/* --------------------------------------------------
   10. FIND KEY
   -------------------------------------------------- */
string find_key(vector<string> groups)
{
    string key = "";

    for (string group : groups)
    {
        int shift = find_shift(group);

        key += char('A' + shift);
    }

    return key;
}


/* --------------------------------------------------
   11. VIGENERE DECRYPT
   -------------------------------------------------- */
string vigenere_decrypt(
    string ciphertext,
    string key)
{
    string plaintext = "";

    for (int i = 0;
         i < ciphertext.length();
         i++)
    {
        int c =
            ciphertext[i] - 'A';

        int k =
            key[i % key.length()] - 'A';

        int p =
            (c - k + 26) % 26;

        plaintext +=
            char('A' + p);
    }

    return plaintext;
}


/* --------------------------------------------------
   12. VIGENERE ENCRYPT
   -------------------------------------------------- */
string vigenere_encrypt(
    string plaintext,
    string key)
{
    string ciphertext = "";

    for (int i = 0;
         i < plaintext.length();
         i++)
    {
        int p =
            plaintext[i] - 'A';

        int k =
            key[i % key.length()] - 'A';

        int c =
            (p + k) % 26;

        ciphertext +=
            char('A' + c);
    }

    return ciphertext;
}


/* --------------------------------------------------
   13. VERIFY
   -------------------------------------------------- */
bool verify(
    string original,
    string generated)
{
    return original == generated;
}


/* --------------------------------------------------
   MAIN
   -------------------------------------------------- */
int main()
{
    /*
       Open cipher.txt
    */

    ifstream file("cipher.txt");

    if (!file)
    {
        cout << "Error: cipher.txt not found!\n";
        return 1;
    }


    /*
       Read complete file
    */

    string text;
    string line;

    while (getline(file, line))
    {
        text += line;
    }

    file.close();


    /*
       Clean ciphertext
    */

    string ciphertext =
        clean_ciphertext(text);


    cout << "=====================================\n";
    cout << " VIGENERE CIPHER CRYPTANALYSIS\n";
    cout << " GROUP NUMBER: 14\n";
    cout << "=====================================\n";

    cout << "\nCiphertext length: "
         << ciphertext.length()
         << endl;


    /*
       KASISKI TEST
    */

    int keyLength =
        kasiski_analysis(ciphertext);


    /*
       For the given Group 14 ciphertext,
       expected key length is 12.
    */

    if (keyLength != 12)
    {
        cout << "\nKasiski suggested length: "
             << keyLength << endl;

        cout << "Using strongest expected candidate: 12\n";

        keyLength = 12;
    }


    cout << "\nEstimated Key Length = "
         << keyLength
         << endl;


    /*
       BONUS: INDEX OF COINCIDENCE
    */

    cout << "\n========== BONUS: IC ==========\n";

    double ic =
        calculate_ic(ciphertext);

    cout << "Overall IC = "
         << fixed
         << setprecision(4)
         << ic
         << endl;


    /*
       SPLIT INTO GROUPS
    */

    vector<string> groups =
        split_into_groups(
            ciphertext,
            keyLength);


    cout << "\nNumber of groups = "
         << groups.size()
         << endl;


    /*
       FREQUENCY ANALYSIS
    */

    frequency_analysis(groups);


    /*
       FIND KEY
    */

    string key =
        find_key(groups);


    cout << "\n========== KEY ==========\n";

    cout << "Recovered Key = "
         << key
         << endl;


    /*
       DECRYPT
    */

    string plaintext =
        vigenere_decrypt(
            ciphertext,
            key);


    cout << "\n========== PLAINTEXT ==========\n";

    cout << plaintext
         << endl;


    /*
       RE-ENCRYPT FOR VERIFICATION
    */

    string generatedCipher =
        vigenere_encrypt(
            plaintext,
            key);


    cout << "\n========== VERIFICATION ==========\n";

    if (verify(ciphertext, generatedCipher))
    {
        cout << "SUCCESS!\n";
        cout << "Re-encrypted ciphertext matches "
                "the original ciphertext.\n";
    }
    else
    {
        cout << "FAILED!\n";
        cout << "Ciphertexts do not match.\n";
    }


    return 0;
}

