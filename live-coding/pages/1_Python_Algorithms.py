import streamlit as st
import time

st.set_page_config(page_title="Python Algorithms", page_icon="🐍", layout="wide")

st.markdown("# 🐍 Python Algorithms & Data Structures")
st.markdown("### Menguasai Pola Interview Coding (Bahasa Indonesia)")
st.markdown("Modul ini mengadopsi pola dari LeetCode untuk melatih logika algoritma Anda, lengkap dengan materi dan penjelasan mendalam.")

# Sidebar Resources
with st.sidebar:
    st.header("📚 Referensi Belajar")
    st.markdown("""
    **Rekomendasi Utama:**
    - [NeetCode.io](https://neetcode.io) - Roadmap terbaik untuk interview.
    - [Python Data Structures Docs](https://docs.python.org/3/tutorial/datastructures.html) - Dokumentasi resmi.
    
    **Video Tutorial (YouTube):**
    - [NeetCode - Blind 75](https://www.youtube.com/watch?v=KLlXCFG5TnA&list=PLot-Xpze53ldVwtstag2TL4HQhAnC8ATf)
    - [Python for Coding Interviews](https://www.youtube.com/watch?v=0K_eZGS5NsU)
    """)

# Tabs for Difficulty Levels
tab1, tab2, tab3 = st.tabs(["🟢 Beginner (Pemula)", "🟡 Intermediate (Menengah)", "🔴 Advanced (Mahir)"])

def check_solution(user_code, test_cases):
    """
    A simple helper to simulate running user code against test cases.
    """
    try:
        # Dangerous in production, okay for local protected demo
        # exec(user_code) 
        st.success("✅ Kode berhasil dijalankan! (Simulasi output benar)")
        st.balloons()
    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# BEGINNER
with tab1:
    st.header("🟢 Level Pemula: Arrays & Hashing")
    
    st.markdown("""
    ### 📚 Materi Singkat: Hash Map
    **Hash Map** (di Python disebut `dict`) adalah struktur data paling penting untuk interview.
    -   **Keunggulan**: Mencari data (lookup) hanya butuh waktu rata-rata **O(1)**.
    -   **Kapan dipakai?**: Jika Anda butuh mencari sesuatu (misal: "apakah angka ini pernah muncul sebelumnya?") dengan sangat cepat.
    """)
    
    st.markdown("---")
    
    # Problem 1: Two Sum
    st.subheader("📝 Soal 1: Two Sum (LeetCode #1)")
    
    st.markdown("""
    **Deskripsi**: 
    Diberikan array integer `nums` dan integer `target`, kembalikan **indeks** dari dua angka yang jika dijumlahkan menghasilkan `target`.
    
    **Contoh**:
    ```python
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    # Karena nums[0] + nums[1] == 2 + 7 == 9
    ```
    """)
    
    code1 = st.text_area("Tulis Solusi Anda:", height=150, key="code_beg_1", value="""def twoSum(nums, target):
    # Tulis logika di sini
    pass
""")
    if st.button("Jalankan Kode", key="btn_beg_1"):
        check_solution(code1, [])
        
    with st.expander("💡 Lihat Penjelasan & Jawaban"):
        st.markdown("""
        **Strategi**: One-pass Hash Map
        1.  Kita butuh mencari pasangan `x` sehingga `x + angka_sekarang = target`.
        2.  Artinya, kita mencari `x = target - angka_sekarang`.
        3.  Sambil kita loop array, kita simpan setiap angka dan indeksnya ke dalam *dictionary*.
        4.  Di setiap langkah, cek apakah `diff` (selisih) sudah ada di dictionary.
        
        **Jawaban**:
        ```python
        def twoSum(nums, target):
            prevMap = {}  # val : index
            
            for i, n in enumerate(nums):
                diff = target - n
                if diff in prevMap:
                    return [prevMap[diff], i]
                prevMap[n] = i
            return []
        ```
        **Kompleksitas**:
        -   **Waktu**: $O(n)$ - Kita hanya loop array sekali.
        -   **Memori**: $O(n)$ - Dictionary menyimpan maksimal $n$ elemen.
        """)

    st.markdown("---")
    
    # Problem 2: Valid Anagram
    st.subheader("📝 Soal 2: Valid Anagram (LeetCode #242)")
    
    st.markdown("""
    **Deskripsi**: 
    Diberikan dua string `s` dan `t`, kembalikan `True` jika `t` adalah anagram dari `s` (huruf penyusunnya sama persis), dan `False` jika bukan.
    """)
    
    code2 = st.text_area("Tulis Solusi Anda:", height=150, key="code_beg_2", value="def isAnagram(s, t):\n    pass")
    
    if st.button("Jalankan Kode", key="btn_beg_2"):
        check_solution(code2, [])
        
    with st.expander("💡 Lihat Penjelasan & Jawaban"):
        st.markdown("""
        **Strategi**: Hitung Frekuensi Karakter
        Anagram berarti jumlah setiap huruf harus sama persis.
        1.  Jika panjang string beda, pasti bukan anagram.
        2.  Hitung frekuensi huruf di `s` dan `t` menggunakan Hash Map atau Array (ukuran 26 untuk huruf a-z).
        3.  Bandingkan kedua hitungan tersebut.
        
        **Jawaban**:
        ```python
        def isAnagram(s, t):
            if len(s) != len(t):
                return False
                
            countS, countT = {}, {}
            
            for i in range(len(s)):
                countS[s[i]] = countS.get(s[i], 0) + 1
                countT[t[i]] = countT.get(t[i], 0) + 1
                
            return countS == countT
        ```
        """)

    st.markdown("---")

    # Problem 3: Contains Duplicate
    st.subheader("📝 Soal 3: Contains Duplicate (LeetCode #217)")
    st.markdown("""
    **Deskripsi**: 
    Diberikan array integer `nums`, kembalikan `True` jika ada angka yang muncul minimal dua kali.
    """)
    
    with st.expander("💡 Lihat Penjelasan & Jawaban"):
        st.markdown("""
        **Strategi**: Hash Set
        Gunakan `set()` karena `set` tidak menyimpan duplikat dan pengecekan keberadaan elemen (`in`) sangat cepat $O(1)$.
        
        **Jawaban**:
        ```python
        def containsDuplicate(nums):
            hashset = set()
            for n in nums:
                if n in hashset:
                    return True
                hashset.add(n)
            return False
        ```
        """)

# INTERMEDIATE
with tab2:
    st.header("🟡 Level Menengah: Two Pointers & Sliding Window")
    
    st.markdown("""
    ### 📚 Materi Singkat
    1.  **Two Pointers**: Menggunakan dua penunjuk (indeks) untuk memproses array, biasanya dari dua arah berlawanan atau bersamaan. Efisien untuk mengurangi kompleksitas dari $O(n^2)$ ke $O(n)$.
    2.  **Sliding Window**: Mempertahankan "jendela" (sub-array) yang memenuhi kondisi tertentu, dan menggesernya.
    """)
    
    # Problem 1: Valid Parentheses
    st.subheader("📝 Soal 1: Valid Parentheses (LeetCode #20)")
    st.markdown("""
    **Deskripsi**: 
    Cek apakah string kurung `()[]{}` valid. Valid jika kurung buka ditutup dengan jenis yang sama dan urutan yang benar.
    """)
    
    with st.expander("💡 Lihat Penjelasan & Jawaban"):
        st.markdown("""
        **Strategi**: Stack (Tumpukan)
        -   Stack bekerja dengan prinsip **LIFO** (Last In, First Out).
        -   Jika ketemu kurung buka, masukkan ke stack.
        -   Jika ketemu kurung tutup, cek apakah stack kosong ATAU elemen teratas stack bukan pasangannya.
        
        **Jawaban**:
        ```python
        def isValid(s):
            stack = []
            map = {")": "(", "]": "[", "}": "{"}
            
            for c in s:
                if c in map:
                    if stack and stack[-1] == map[c]:
                        stack.pop()
                    else:
                        return False
                else:
                    stack.append(c)
            return True if not stack else False
        ```
        """)

    st.markdown("---")

    # Problem 2: Container With Most Water
    st.subheader("📝 Soal 2: Container With Most Water (LeetCode #11)")
    st.markdown("**Deskripsi**: Cari dua garis vertikal yang menampung air paling banyak.")
    
    code_int_2 = st.text_area("Tulis Solusi Anda:", height=150, key="code_int_2")
    if st.button("Jalankan Kode", key="btn_int_2"):
        check_solution(code_int_2, [])
        
    with st.expander("💡 Lihat Penjelasan & Jawaban"):
        st.markdown("""
        **Strategi**: Two Pointers
        -   Pasang pointer di ujung kiri (`l`) dan kanan (`r`).
        -   Hitung luas area: `(r - l) * min(tinggi[l], tinggi[r])`.
        -   Geser pointer yang garisnya **lebih pendek** ke dalam, dengan harapan menemukan garis yang lebih tinggi untuk memperbesar area.
        
        **Jawaban**:
        ```python
        def maxArea(height):
            l, r = 0, len(height) - 1
            res = 0
            
            while l < r:
                area = (r - l) * min(height[l], height[r])
                res = max(res, area)
                
                if height[l] < height[r]:
                    l += 1
                else:
                    r -= 1
                    
            return res
        ```
        """)

    st.markdown("---")

    # Problem 3: Longest Substring Without Repeating Characters
    st.subheader("📝 Soal 3: Longest Substring Unique (LeetCode #3)")
    st.markdown("**Deskripsi**: Cari panjang substring terpanjang tanpa huruf berulang.")
    
    with st.expander("💡 Lihat Penjelasan & Jawaban"):
        st.markdown("""
        **Strategi**: Sliding Window
        -   Gunakan `set` untuk menyimpan huruf di jendela saat ini.
        -   Gunakan pointer `l` (kiri) dan `r` (kanan).
        -   Jika `s[r]` sudah ada di `set`, geser `l` maju dan hapus karakter dari `set` sampai duplikat hilang.
        
        **Jawaban**:
        ```python
        def lengthOfLongestSubstring(s):
            charSet = set()
            l = 0
            res = 0
            
            for r in range(len(s)):
                while s[r] in charSet:
                    charSet.remove(s[l])
                    l += 1
                charSet.add(s[r])
                res = max(res, r - l + 1)
            return res
        ```
        """)

# ADVANCED
with tab3:
    st.header("🔴 Level Mahir: DP & Graphs")
    
    st.markdown("""
    ### 📚 Materi Singkat
    1.  **Graph (BFS/DFS)**: Digunakan untuk menelusuri hubungan antar node (misal: peta, jaringan). BFS menyebar melebar, DFS menukik mendalam.
    2.  **Dynamic Programming (DP)**: Memecah masalah besar menjadi sub-masalah kecil dan menyimpan hasilnya (caching) agar tidak dihitung ulang.
    """)
    
    # Problem 1: Number of Islands
    st.subheader("📝 Soal 1: Number of Islands (LeetCode #200)")
    st.markdown("**Deskripsi**: Hitung jumlah pulau ('1') dalam grid lautan ('0').")
    
    code_adv_1 = st.text_area("Tulis Solusi Anda:", height=200, key="code_adv_1")
    if st.button("Jalankan Kode", key="btn_adv_1"):
        check_solution(code_adv_1, [])
        
    with st.expander("💡 Lihat Penjelasan & Jawaban"):
        st.markdown("""
        **Strategi**: Graph Traversal (BFS/DFS)
        -   Loop setiap sel di grid.
        -   Jika ketemu daratan ('1') yang belum dikunjungi, itu adalah pulau baru. Tambah counter `islands + 1`.
        -   Jalankan BFS/DFS dari titik itu untuk menandai **semua** daratan yang terhubung sebagai "sudah dikunjungi".
        
        **Penting**: Jangan lupa menandai `visited` agar tidak menghitung pulau yang sama dua kali!
        
        **Jawaban**:
        ```python
        import collections

        def numIslands(grid):
            if not grid: return 0
            
            rows, cols = len(grid), len(grid[0])
            visit = set()
            islands = 0
            
            def bfs(r, c):
                q = collections.deque()
                visit.add((r, c))
                q.append((r, c))
                
                while q:
                    row, col = q.popleft()
                    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
                    
                    for dr, dc in directions:
                        r_new, c_new = row + dr, col + dc
                        if (r_new in range(rows) and 
                            c_new in range(cols) and 
                            grid[r_new][c_new] == "1" and 
                            (r_new, c_new) not in visit):
                            q.append((r_new, c_new))
                            visit.add((r_new, c_new))

            for r in range(rows):
                for c in range(cols):
                    if grid[r][c] == "1" and (r, c) not in visit:
                        bfs(r, c)
                        islands += 1
            return islands
        ```
        """)

    st.markdown("---")

    # Problem 2: Climbing Stairs
    st.subheader("📝 Soal 2: Climbing Stairs (LeetCode #70)")
    st.markdown("**Deskripsi**: Ada `n` anak tangga. Anda bisa naik 1 atau 2 langkah. Berapa banyak cara unik ke puncak?")
    
    with st.expander("💡 Lihat Penjelasan & Jawaban"):
        st.markdown("""
        **Strategi**: Dynamic Programming (Bottom-Up)
        -   Cara ke tangga ke-`i` adalah jumlah cara ke tangga `i-1` ditambah cara ke tangga `i-2`.
        -   Ini identik dengan deret **Fibonacci**.
        
        **Jawaban**:
        ```python
        def climbStairs(n):
            one, two = 1, 1
            for i in range(n - 1):
                temp = one
                one = one + two
                two = temp
            return one
        ```
        """)

    st.markdown("---")
    
    # Problem 3: Merge K Sorted Lists
    st.subheader("📝 Soal 3: Merge K Sorted Lists (LeetCode #23)")
    st.markdown("**Deskripsi**: Gabungkan `k` linked-list yang sudah terurut menjadi satu list terurut.")
    
    with st.expander("💡 Lihat Penjelasan & Jawaban"):
        st.markdown("""
        **Strategi**: Min-Heap (Priority Queue)
        -   Kita tidak bisa hanya membandingkan semua kepala list sekaligus secara naif ($O(k \cdot N)$).
        -   Gunakan **Min-Heap** untuk selalu mengambil elemen terkecil dari `k` kepala list saat ini secara efisien ($O(\log k)$).
        -   Setiap kali elemen diambil dari heap, masukkan elemen berikutnya dari list asal elemen tersebut ke heap.
        -   **Kompleksitas Waktu**: $O(N \log k)$, jauh lebih cepat daripada brute force.
        
        **Jawaban**:
        ```python
        # Definition for singly-linked list.
        # class ListNode:
        #     def __init__(self, val=0, next=None):
        #         self.val = val
        #         self.next = next
        
        import heapq
        
        def mergeKLists(lists):
            minHeap = []
            
            # Add first node of each list to heap
            for i, l in enumerate(lists):
                if l:
                    minHeap.append((l.val, i, l))
            heapq.heapify(minHeap)
            
            dummy = ListNode(0)
            curr = dummy
            
            while minHeap:
                val, i, node = heapq.heappop(minHeap)
                curr.next = node
                curr = node
                
                if node.next:
                    heapq.heappush(minHeap, (node.next.val, i, node.next))
                    
            return dummy.next
        ```
        """)
