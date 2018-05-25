SELECT * FROM dbo.NhaCungCap
USE QLMobileStore

-- Câu 1: Truy vấn từ 1 bảng sử dụng orderby
SELECT * FROM dbo.PhieuNhap ORDER BY NgayNhap ASC
-- Câu 2: Thực hiện thủ tục update dữ liệu
GO
CREATE PROC SuaDuLieuNhaCC (@Ma VARCHAR(9), @TenNhaCC nvarchar(100),@DiaChi nvarchar(150),@Sdt varchar(15))
As
BEGIN
	IF LEN(@Sdt)<15 AND  LEN(@Ma)>0
	BEGIN
		UPDATE dbo.NhaCungCap SET MaNhaCC=@Ma,TenNhaCC=@TenNhaCC,DiaChi=@DiaChi,Sdt=@Sdt WHERE MaNhaCC=@Ma
	END
END
GO
EXEC dbo.SuaDuLieuNhaCC @Ma='NhaCC8', @TenNhaCC ='Nhật Cường',@DiaChi='Hà Nội',@Sdt=0973642632



GO
-- Câu 3: Thực hiện thủ tục update dữ liệu từ 2 bảng có giàng buộc

 SELECT  NhaSanXuat.TenNSX,MaNhaSX, COUNT(MaNhaSX)  AS SoLuong ,SUM(GiaThanh) GiaTheoSoLuong
        FROM dbo.ThietBi 
			 JOIN dbo.NhaSanXuat ON NhaSanXuat.MaNSX = ThietBi.MaNhaSX
		GROUP BY MaNhaSX,TenNSX 
-- Câu 4.a: Thực hiện thủ tục update dữ liệu

--Thêm
ALTER PROC ThemChiTietPhieNhap (@MaPN VARCHAR(9),@MaNV VARCHAR(9),@MaTB VARCHAR(9),@MaNhaCC VARCHAR(9),@SoLuong INT ,@GiaThanh FLOAT)
As
BEGIN
	DECLARE @sl INT
	SELECT @sl= COUNT(dbo.PhieuNhap.MaPN) FROM dbo.PhieuNhap WHERE MaPN=@MaPN
	IF @sl=0
	BEGIN
		INSERT dbo.PhieuNhap
				( MaPN, MaNV, MaNhaCC, NgayNhap )
		VALUES  ( @MaPN, -- MaPN - varchar(9)
				  @MaNV, -- MaNV - varchar(9)
				  @MaNhaCC, -- MaNhaCC - varchar(9)
				  GETDATE()  -- NgayNhap - date
				  )
	END
	INSERT dbo.CTPhieuNhap
	        ( MaPN, MaTB, SoLuong, DonGia )
	VALUES  ( @MaPN, -- MaPN - varchar(9)
	          @MaTB, -- MaTB - varchar(9)
	          @SoLuong, -- SoLuong - int
	          @SoLuong*@GiaThanh  -- DonGia - float
	          )
END

EXEC dbo.ThemChiTietPhieNhap @MaPN = 'PN24', -- varchar(9)
    @MaNV = 'NV5', -- varchar(9)
    @MaTB = 'TB8', -- varchar(9)
    @MaNhaCC = 'NhaCC6', -- varchar(9)
    @SoLuong = 10, -- int
    @GiaThanh = 229.99 -- int


--Xóa Phiếu Xuất

CREATE PROC XoaPhieuNhap (@MaPN VARCHAR(9))
As
BEGIN
	DELETE dbo.CTPhieuNhap WHERE MaPN=@MaPN
	DELETE dbo.PhieuNhap WHERE MaPN=@MaPN
END
GO

EXEC XoaPhieuNhap @MaPN='PN21'


-- Câu 4.b: Thực hiện thủ tục update dữ liệu trên view
DROP VIEW dbo.v_THongKeNhaCC
CREATE VIEW v_THongKeNhaCC
AS
    SELECT  TenNhaCC ,
            COUNT(ThietBi.MaNhaCC) AS SoLuong
    FROM    dbo.ThietBi
            JOIN dbo.NhaCungCap ON NhaCungCap.MaNhaCC = ThietBi.MaNhaCC
    GROUP BY TenNhaCC 



-- Tạo ra view những nhân viên đã xuất hàng
CREATE VIEW v_NhanVienXuat
AS
    SELECT  NhanVien.MaNV ,
            HoTenNV ,
            NgaySinh ,
            DiaChi ,
            Sdt ,
            PhieuNhap.MaPN
    FROM    dbo.NhanVien
            JOIN dbo.PhieuNhap ON PhieuNhap.MaNV = NhanVien.MaNV
    WHERE   PhieuNhap.MaNV IN ( SELECT  MaNV
                                FROM    dbo.PhieuXuat )        
  
GO
-- Tạo ra view v_NhanVienXuat 
UPDATE v_NhanVienXuat SET HoTenNV = 'Ngô Đình Phúc' WHERE MaNV= 'NV3'

INSERT dbo.CTPhieuNhap
        ( MaPN, MaTB, SoLuong, DonGia )
VALUES  ( '', -- MaPN - varchar(9)
          '', -- MaTB - varchar(9)
          0, -- SoLuong - int
          0.0  -- DonGia - float
          )