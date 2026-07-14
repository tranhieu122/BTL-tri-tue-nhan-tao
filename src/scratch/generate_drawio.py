import os

def create_system_flow_xml():
    xml = """<mxfile host="Electron" modified="2026-07-11T13:13:19.000Z" agent="Mozilla/5.0" version="21.6.8" type="device">
  <diagram id="system_flow_diagram" name="System Flow">
    <mxGraphModel dx="1200" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- Nodes -->
        <mxCell id="n1" value="Người dùng chọn Start, End, Thuật toán &amp;amp; bấm 'Tìm đường'" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="300" y="40" width="220" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="n2" value="Frontend gọi hàm findPath() trong algorithms.js" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="300" y="150" width="220" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="n3" value="Gửi HTTP POST request tới /api/pathfind" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="300" y="260" width="220" height="50" as="geometry" />
        </mxCell>
        
        <mxCell id="n4" value="Flask app.py nhận request &amp;amp; điều phối xử lý" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="300" y="360" width="220" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="n5" value="Cập nhật trạng thái chướng ngại vật trong VietnamGraph (NetworkX)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9663e8;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="140" y="470" width="220" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="n6" value="Lưu lịch sử truy vấn vào bảng search_history (SQLite)" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="460" y="460" width="180" height="80" as="geometry" />
        </mxCell>
        
        <mxCell id="n7" value="Thực thi thuật toán tìm kiếm được chọn trong /algorithms" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9663e8;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="140" y="580" width="220" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="n8" value="Đo thời gian thực thi trung bình bằng cách chạy 10 lần" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9663e8;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="140" y="690" width="220" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="n9" value="Trả về JSON chứa path, cost, exploration_steps, time_ms" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="300" y="800" width="220" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="n10" value="Frontend (visualization.js) chạy hoạt ảnh từng bước duyệt trên SVG" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="300" y="910" width="220" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="n11" value="Hiển thị kết quả đường đi tối ưu và cập nhật bảng so sánh" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="300" y="1020" width="220" height="60" as="geometry" />
        </mxCell>

        <!-- Edges -->
        <mxCell id="e1" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="n1" target="n2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="e2" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="n2" target="n3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="e3" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="n3" target="n4">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="e4" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="n4" target="n5">
          <mxGeometry relative="1" as="geometry">
            <Array points="410,440", "250,440" />
          </mxGeometry>
        </mxCell>
        
        <mxCell id="e5" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;entrySz=15;" edge="1" parent="1" source="n4" target="n6">
          <mxGeometry relative="1" as="geometry">
            <Array points="410,440", "550,440" />
          </mxGeometry>
        </mxCell>
        
        <mxCell id="e6" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="n5" target="n7">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="e7" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="n7" target="n8">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="e8" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="n8" target="n9">
          <mxGeometry relative="1" as="geometry">
            <Array points="250,770", "300,770" />
          </mxGeometry>
        </mxCell>
        
        <mxCell id="e9" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;exitPerimeter=1;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="n6" target="n9">
          <mxGeometry relative="1" as="geometry">
            <Array points="550,770", "520,770" />
          </mxGeometry>
        </mxCell>
        
        <mxCell id="e10" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="n9" target="n10">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="e11" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="n10" target="n11">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    return xml

def create_search_flow_xml():
    xml = """<mxfile host="Electron" modified="2026-07-11T13:13:19.000Z" agent="Mozilla/5.0" version="21.6.8" type="device">
  <diagram id="search_algorithm_diagram" name="Search Algorithm">
    <mxGraphModel dx="1200" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- Nodes -->
        <mxCell id="s1" value="Bắt đầu tìm kiếm" style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="320" y="40" width="160" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="s2" value="Khởi tạo Open List (hàng đợi ưu tiên) chứa nút Start&lt;br&gt;Khởi tạo Closed List (tập đã duyệt) rỗng" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9663e8;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="275" y="140" width="250" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="s3" value="Thuật toán cần&lt;br&gt;Heuristic?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="310" y="240" width="180" height="80" as="geometry" />
        </mxCell>
        
        <mxCell id="s4" value="Tính h(n) bằng khoảng cách Haversine * 0.6" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="180" y="360" width="180" height="50" as="geometry" />
        </mxCell>
        
        <mxCell id="s5" value="Đặt Heuristic h(n) = 0" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="440" y="360" width="180" height="50" as="geometry" />
        </mxCell>
        
        <mxCell id="s6" value="Open List rỗng?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="310" y="460" width="180" height="80" as="geometry" />
        </mxCell>
        
        <mxCell id="s7" value="Không tìm thấy đường&lt;br&gt;(Thất bại)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="580" y="470" width="180" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="s8" value="Lấy nút n có f(n) nhỏ nhất ra khỏi Open List&lt;br&gt;(f = g + h)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="275" y="580" width="250" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="s9" value="n đã thuộc&lt;br&gt;Closed List?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="310" y="680" width="180" height="80" as="geometry" />
        </mxCell>
        
        <mxCell id="s10" value="Đưa n vào Closed List&lt;br&gt;Ghi nhận bước duyệt vào exploration_steps" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="275" y="800" width="250" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="s11" value="n == End (Đích)?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="310" y="900" width="180" height="80" as="geometry" />
        </mxCell>
        
        <mxCell id="s12" value="Đo thời gian chạy trung bình &amp;amp; Trả về đường đi tối ưu cùng chi phí (Thành công)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="580" y="910" width="200" height="60" as="geometry" />
        </mxCell>
        
        <mxCell id="s13" value="Duyệt từng nút kề m của n" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="300" y="1020" width="200" height="50" as="geometry" />
        </mxCell>
        
        <mxCell id="s14" value="m đã duyệt OR cạnh n-m bị chặn?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="290" y="1110" width="220" height="80" as="geometry" />
        </mxCell>
        
        <mxCell id="s15" value="Tính chi phí mới: g(m) = g(n) + d(n, m)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="300" y="1230" width="200" height="50" as="geometry" />
        </mxCell>
        
        <mxCell id="s16" value="g(m) tốt hơn&lt;br&gt;chi phí cũ?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="310" y="1320" width="180" height="80" as="geometry" />
        </mxCell>
        
        <mxCell id="s17" value="Cập nhật g(m), tính f(m) &amp;amp; Thêm m vào Open List" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9663e8;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="290" y="1440" width="220" height="50" as="geometry" />
        </mxCell>

        <!-- Edges -->
        <mxCell id="es1" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s1" target="s2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="es2" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s2" target="s3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="es3" value="Có" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="s3" target="s4">
          <mxGeometry relative="1" as="geometry">
            <Array points="270,280", "270,360" />
          </mxGeometry>
        </mxCell>
        
        <mxCell id="es4" value="Không" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="s3" target="s5">
          <mxGeometry relative="1" as="geometry">
            <Array points="530,280", "530,360" />
          </mxGeometry>
        </mxCell>
        
        <mxCell id="es5" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="s4" target="s6">
          <mxGeometry relative="1" as="geometry">
            <Array points="270,430", "400,430" />
          </mxGeometry>
        </mxCell>
        
        <mxCell id="es6" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="s5" target="s6">
          <mxGeometry relative="1" as="geometry">
            <Array points="530,430", "400,430" />
          </mxGeometry>
        </mxCell>
        
        <mxCell id="es7" value="Đúng" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s6" target="s7">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="es8" value="Sai" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s6" target="s8">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="es9" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s8" target="s9">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="es10" value="Đúng" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;" edge="1" parent="1" source="s9">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="400" y="440" as="targetPoint"/>
            <Array points="120,720", "120,440" />
          </mxGeometry>
        </mxCell>
        
        <mxCell id="es11" value="Sai" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s9" target="s10">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="es12" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s10" target="s11">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="es13" value="Đúng" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s11" target="s12">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="es14" value="Sai" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s11" target="s13">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="es15" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s13" target="s14">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="es16" value="Đúng" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0;exitY=0.5;exitDx=0;exitDy=0;" edge="1" parent="1" source="s14">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="400" y="1000" as="targetPoint"/>
            <Array points="250,1150", "250,1000" />
          </mxGeometry>
        </mxCell>
        
        <mxCell id="es17" value="Sai" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s14" target="s15">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="es18" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s15" target="s16">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="es19" value="Đúng" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="s16" target="s17">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <mxCell id="es20" value="Sai" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;" edge="1" parent="1" source="s16">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="400" y="1000" as="targetPoint"/>
            <Array points="550,1360", "550,1000" />
          </mxGeometry>
        </mxCell>
        
        <mxCell id="es21" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;" edge="1" parent="1" source="s17">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="400" y="1000" as="targetPoint"/>
            <Array points="400,1520", "550,1520", "550,1000" />
          </mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    return xml

def main():
    target_dir = r"c:\Users\thesh\Ki 1 2026-2027\Artificial Intelligence\src\draw.io"
    os.makedirs(target_dir, exist_ok=True)
    
    system_flow_path = os.path.join(target_dir, "system_flow.drawio")
    with open(system_flow_path, "w", encoding="utf-8") as f:
        f.write(create_system_flow_xml())
    print(f"Generated: {system_flow_path}")
    
    search_flow_path = os.path.join(target_dir, "search_algorithm_flow.drawio")
    with open(search_flow_path, "w", encoding="utf-8") as f:
        f.write(create_search_flow_xml())
    print(f"Generated: {search_flow_path}")

if __name__ == '__main__':
    main()
