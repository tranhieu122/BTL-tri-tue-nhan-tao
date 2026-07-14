import heapq

# Đồ thị
do_thi = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('D', 5), ('E', 2)],
    'C': [('A', 4), ('E', 1)],
    'D': [('B', 5), ('E', 1)],
    'E': [('B', 2), ('C', 1), ('D', 1)]
}

# Hàm heuristic (ước lượng khoảng cách đến đích)
ham_uoc_luong = {
    'A': 3,
    'B': 2,
    'C': 1,
    'D': 1,
    'E': 0
}

def a_star(diem_bat_dau, diem_dich):

    # heapq là hàng đợi ưu tiên (Priority Queue)
    hang_doi = []

    # Đưa điểm bắt đầu vào hàng đợi
    heapq.heappush(hang_doi, (0, diem_bat_dau))

    # g(n): chi phí từ điểm bắt đầu đến node hiện tại
    chi_phi = {
        diem_bat_dau: 0
    }

    # Lưu cha để truy vết đường đi
    nut_cha = {}

    while hang_doi:

        # Lấy node có f nhỏ nhất
        f, nut_hien_tai = heapq.heappop(hang_doi)

        if nut_hien_tai == diem_dich:
            break

        # Duyệt các đỉnh kề
        for nut_ke, trong_so in do_thi[nut_hien_tai]:

            chi_phi_moi = chi_phi[nut_hien_tai] + trong_so

            # Nếu tìm được đường đi tốt hơn
            if nut_ke not in chi_phi or chi_phi_moi < chi_phi[nut_ke]:

                chi_phi[nut_ke] = chi_phi_moi

                # f = g + h
                tong_chi_phi = chi_phi_moi + ham_uoc_luong[nut_ke]

                heapq.heappush(hang_doi, (tong_chi_phi, nut_ke))

                nut_cha[nut_ke] = nut_hien_tai

    # Truy vết đường đi
    duong_di = []

    nut = diem_dich

    while nut != diem_bat_dau:
        duong_di.append(nut)
        nut = nut_cha[nut]

    duong_di.append(diem_bat_dau)
    duong_di.reverse()

    print("Đường đi:", duong_di)
    print("Tổng chi phí:", chi_phi[diem_dich])


a_star("A", "E")