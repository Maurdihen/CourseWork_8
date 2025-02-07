import json
from api.hh_api import HeadHunterAPI
from db.create_table import create_tables
from db.insert_db import insert_data


def main() -> None:
    """
    Main function to fetch company data from HeadHunter API, save it to a JSON file,
    create the necessary database tables, and insert the data into the database.

    The function performs the following steps:
    1. Fetches company data from the HeadHunter API.
    2. Saves the fetched data to a JSON file.
    3. Creates the 'employers' and 'vacancies' tables in the database.
    4. Inserts the data from the JSON file into the database.

    Returns:
        None
    """
    url: str = "https://api.hh.ru/employers"
    hh_api: HeadHunterAPI = HeadHunterAPI(url)
    companies: dict = hh_api.get_data({'cnt_employers': 50, "search_text": ""})

    with open('companies.json', 'w', encoding='utf-8') as f:
        json.dump(companies, f, ensure_ascii=False)

    create_tables()
    insert_data()


if __name__ == "__main__":
    main()
A

#include <iostream>
#include <vector>
#include <deque>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr); 
    cout.tie(nullptr);
    int n, k; cin >> n >> k;
    vector<int> arr;
    for (int i = 0; i < n; ++i) {
        int temp; cin >> temp;
        arr.push_back(temp);
    }
    deque<int> deq;
    for (int i = 0; i < n; ++i) {
        if (!deq.empty()) {
            while (!deq.empty() && arr[i] < deq.back()) {
                deq.pop_back();
            }
            deq.push_back(arr[i]);
        } else {
            deq.push_back(arr[i]);
        }
        if (i >= k - 1) {
            cout << deq.front() << "\n";
            if (arr[i - k + 1] == deq.front()) {
                deq.pop_front();
            }
        }
    }
    return 0;
}


B

#include <vector>
#include <iostream>
#include <algorithm>

using namespace std;

#define int long long

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> arr(n);
    for (auto &i: arr) cin >> i;
    sort(arr.begin(), arr.end());
    int ans = 0;
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            int temp = arr[i] + arr[j];
            auto it = lower_bound(arr.begin(), arr.end(), temp) - arr.begin();
            it--;
            ans += it - j;
        }
    }
    cout << ans;
}

C

n = int(input())

dp = []

for i in range(2 * n - 1, n - 1, -1):
    dp.append([0] * i)
    dp[-1][0] = 1

for i in range(1, 2 * n - 1):
    for j in range(len(dp)):
        if len(dp[j]) > i:
            if j == 0:
                dp[j][i] = dp[j][i - 1] + 2 * dp[j + 1][i - 1]
            elif j == len(dp) - 1:
                dp[j][i] = dp[j][i - 1] + dp[j - 1][i]
            else:
                dp[j][i] = dp[j][i - 1] + dp[j + 1][i - 1] + dp[j - 1][i]

print(dp[0][2 * n - 2])


D

#include <iostream>
#include <vector>
#include <map>
#include <climits>

using namespace std;

#define INF INT_MAX

map<char, char> buckets;
string s;
vector<vector<int>> dp;
vector<vector<int>> seq;

int ans(int l, int r) {
    if (dp[l][r] != INF) return dp[l][r];
    if (buckets[s[l-1]] == s[r-1]) {
        dp[l][r] = min(dp[l][r], ans(l + 1, r - 1));
        seq[l][r] = -1;
    }
    for (int c = l; c < r; c++) {
        if (ans(l, c) + ans(c + 1, r) < dp[l][r]) {
            dp[l][r] = ans(l, c) + ans(c + 1, r);
            seq[l][r] = c;
        }
    }
    return dp[l][r];
}

string answer(int l, int r) {
    string ans;
    if (seq[l][r] == 0) {
        if (dp[l][r] != r - l + 1) {
            for (int i = l; i <= r; i++) ans += s[i-1];
        }
        return ans;
    }
    if (seq[l][r] == -1) return s[l-1] + answer(l + 1, r - 1) + s[r-1];
    return answer(l, seq[l][r]) + answer(seq[l][r] + 1, r);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr); cout.tie(nullptr);

    buckets = {
        {'(', ')'},
        {'[', ']'},
        {'{', '}'},
    };

    cin >> s;
    int ls = s.length();
    dp.resize(ls + 1, vector<int>(ls + 1, INF));
    seq.resize(ls + 1, vector<int>(ls + 1, 0));

    for (int i = 1; i <= ls; i++) dp[i][i] = 1;
    for (int i = 1; i <= ls - 1; i++) {
        if (buckets[s[i-1]] == s[i]) dp[i][i+1] = 0;
        else dp[i][i+1] = 2;
    }

    ans(1, ls);
    cout << answer(1, ls);
    return  0;
}


E

from bisect import bisect_left

n = int(input())
arr = list(map(int, input().split()))

len_ = [1] * n
lst = [float('inf')] * n
max_len = 0

for idx, value in enumerate(arr):
    pos = bisect_left(lst, value)
    lst[pos] = value
    len_[idx] = pos + 1
    max_len = max(max_len, len_[idx])

res = []
cur = max_len
temp = float('inf')

for i in range(n - 1, -1, -1):
    if len_[i] == cur and arr[i] < temp:
        res.append(arr[i])
        temp = arr[i]
        cur -= 1

print(max_len)
print(*res[::-1])

F

#include <iostream>
#include <vector>
using namespace std;

typedef vector<vector<int>> Matrix;

Matrix multiply(const Matrix& A, const Matrix& B, int mod) {
    int size = A.size();
    Matrix result(size, vector<int>(size, 0));
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            for (int k = 0; k < size; k++) {
                result[i][j] = (result[i][j] + 1LL * A[i][k] * B[k][j] % mod) % mod;
            }
        }
    }
    return result;
}

Matrix bin_pow(Matrix base, int exp, int mod) {
    int size = base.size();
    Matrix result(size, vector<int>(size, 0));
    for (int i = 0; i < size; i++) result[i][i] = 1;
    while (exp > 0) {
        if (exp % 2) result = multiply(result, base, mod);
        base = multiply(base, base, mod);
        exp /= 2;
    }
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n, s, m;
    cin >> n >> s >> m;
    Matrix mat(n, vector<int>(n));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> mat[i][j];
        }
    }
    
    Matrix result = bin_pow(mat, s, m);
    for (const auto& row : result) {
        for (int val : row) cout << val << " ";
        cout << "\n";
    }
    
    return 0;
}


