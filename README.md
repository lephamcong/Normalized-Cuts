IMAGE SEGMENTATION

Phân chia hình ảnh thành các phân vùng dựa trên phương pháp Normalized Cuts được đề cập trong bài báo "Normalized Cuts and Image Segmentation"[1] của Jianbo Shi và Jitendra Malik

Mã nguồn được tham khảo từ [2], [3], [4] và được điều chỉnh phù hợp với ngôn ngữ lập trình Python 3 phiên bản 3.11.1
Bộ dữ liệu đầu vào là bộ ảnh Kodak[5]

Mã nguồn gồm 2 phần chính:
+ Xử lý với đầu vào là ảnh xám (file graph.py và partition.py) với kết quả minh họa như bên dưới

+ Xử lý với đầu vào là ảnh màu (file rgbgraph.py và rgbpartition.py) với kết quả minh họa như bên dưới

[1]: Jianbo Shi and J. Malik, "Normalized cuts and image segmentation," in IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 22, no. 8, pp. 888-905, Aug. 2000, doi: 10.1109/34.868688.

[2]: https://github.com/vignesh99/Image-Segmentation.git

[3]: https://github.com/vignesh99/Image-Segmentation/tree/master/SampleOutputs

[4]: https://github.com/vignesh99/Image-Segmentation/blob/master/EE5175_Project_EE16B127.pdf

[5]: https://github.com/MohamedBakrAli/Kodak-Lossless-True-Color-Image-Suite.git