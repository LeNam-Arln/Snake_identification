# Snake_identification
Nhận diện các loài rắn

## Giới thiệu
Dự án "Snake Identification" nhằm xây dựng một hệ thống có khả năng nhận diện chính xác các loài rắn thông qua hình ảnh, ứng dụng các kỹ thuật học sâu hiện đại trong lĩnh vực thị giác máy tính (Computer Vision). Mô hình có thể hỗ trợ phân loại rắn độc và không độc, cảnh báo nguy hiểm, phục vụ cho công tác bảo tồn động vật hoang dã, giáo dục sinh học, cũng như hỗ trợ y tế trong xử lý rắn cắn.

## Dữ liệu
Dữ liệu được thu thập thủ công từ nhiều nguồn khác nhau bao gồm hình ảnh trên Internet, tư liệu khoa học, hình ảnh thực tế hoặc các cơ sở dữ liệu công khai. Dữ liệu được chia thành nhiều thư mục, mỗi thư mục tương ứng với một loài rắn cụ thể.

Lưu ý: Dataset các bạn phải tự thu thập.

## Mô hình sử dụng
Mô hình học sâu được sử dụng là EfficientNetB0 – một kiến trúc hiện đại do Google đề xuất, nổi bật bởi khả năng cân bằng tốt giữa độ chính xác và tốc độ xử lý. EfficientNetB0 được huấn luyện trước trên tập ImageNet, sau đó được fine-tune trên tập dữ liệu rắn của dự án.

## Cách sử dụng
Mô hình sau khi huấn luyện được lưu dưới định dạng .h5, có thể được sử dụng thông qua file app.py để nhận diện ảnh mới (Thay .h5 thành của bạn).

## Kết Quả:
![image](https://github.com/user-attachments/assets/77739e73-3631-4a34-b657-b5edc49fff86)



