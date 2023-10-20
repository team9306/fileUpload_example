# 设备程序批量导入--沙同
# 2023-10-20
import os
import time
import zipfile
import requests


# 压缩文件
def main():
    # 指定文件夹路径
    folder_path = "F:\\SPI-031200323"
    # 目标文件夹
    destination_folder_path = "spi_031200323_zip_files"

    # 获取文件夹中的所有文件
    file_list = os.listdir(folder_path)

    # 创建一个文件夹来存放压缩文件
    if not os.path.exists(destination_folder_path):
        os.mkdir(destination_folder_path)

    # 遍历文件列表，为每个文件创建一个独立的压缩文件
    for filename in file_list:
        file_path = os.path.join(folder_path, filename)
        # 仅处理文件，而不是文件夹
        if os.path.isfile(file_path):
            # 创建一个与文件同名的压缩文件
            zip_filename = os.path.splitext(filename)[0] + ".zip"
            zip_path = os.path.join(destination_folder_path, zip_filename)
            # 打开压缩文件并将文件写入
            with zipfile.ZipFile(zip_path, "w") as zipf:
                zipf.write(file_path, os.path.basename(file_path))
    print("压缩完成")
    upload_file(destination_folder_path)


# 确定参数，上传至服务器
def upload_file(destination_folder_path):
    api_url = "http://10.20.34.100:28083/API/pms/equipsoft/uploadEquipSoft"
    file_list = os.listdir(destination_folder_path)
    for filename in file_list:
        file_path = os.path.join(destination_folder_path, filename)
        files = {'file_data': open(file_path, 'rb')}
        r = requests.post(api_url, files=files)
        # 将返回值转为数组字符串
        r = "[" + r.text + "]"
        upload_param(filename, r)
    print("上传完成")


# 请求接口，上传其他参数
def upload_param(programName, programUrl):
    api_url = "http://10.20.34.100:28083/API/pms/equipprogram/add"
    data = {
        "equipNo": "031200323",
        "programName": programName,
        "programUse": "默认用途，批量上传",
        "programVersion": "V1.0",
        "programUrl": programUrl,
        "status": "2",
        "remark": "默认备注，批量上传",
        "createBy": "admin",
    }
    print(data)
    r = requests.post(api_url, data=data)
    print(r.text)


if __name__ == '__main__':
    main()
