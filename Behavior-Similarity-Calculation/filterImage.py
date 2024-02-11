import os
import shutil

# 需要移除（移动到其它文件夹）的图片（或者txt）名字
# specific_overlap_files = ['000014_0063', '000020_0056', '000074_0022', '000522_0020', '000553_0076', '000553_0077', '0005 65_0016', '001099_0049', '001099_0060', '001105_0040', '001329_0032', '003575_0112', '003987_0164', '004517_0004', '0045 17_0007', '004517_0035', '004533_0028', '005733_0004', '005733_0005', '005733_0053', '02_037', '08_054', '130_025', '143 _074', '143_133', '143_189', '149_022', '149_090', '152_093', '162_093', '171_068', '176_050', '181_077', '188_101', '19 1_124', '191_125', '192_067', '201_134', '202_039', '202_041', '209_015', '209_021', '209_050', '212_068', '214_003', '2 14_021', '214_022', '219_065', '219_129', '219_213', '21_111', '224_012', '224_063', '224_064', '224_065', '224_066', '2 29_065', '229_069', '229_131', '229_132', '22_088', '231_037', '232_007', '234_109', '234_189', '235_014', '240_027', '2 44_009', '244_045', '244_046', '246_032', '254_024', '256_015', '256_019', '257_052', '257_053', '257_058', '257_059', ' 25_065', '25_070', '25_071', '25_132', '263_056', '263_060', '263_061', '27_108', '27_109', '28_042', '28_053', '28_074' , '28_076', '28_091', '28_117', '28_123', '30_006', '30_100', '33_045', '33_105', '34_154', '34_175', '38_015', '45_083' , '51_046', '51_054', '51_091', '51_140', '55_044', '55_052', '55_104', '55_109', '55_110', '55_156', '55_157', '55_164' , '55_165', '56_086', '56_087', '56_123', '56_124', '59_061', '59_139', '69_128', '73_043', '73_046', '73_048', '73_068' , '73_069', '80_019', '80_022', '80_023', '80_024', '86_052', '88_133', '89_014', '90_004']
specific_overlap_files = ['005824_0069', '006249_0085', '006287_0073', '006466_0019', '110_073', '110_099', '118_001', '1 18_002', '118_003', '118_007', '118_010', '118_011', '118_012', '118_013', '118_015', '118_025', '118_026', '118_027', ' 118_030', '118_036', '118_037', '118_038', '122_017', '122_018', '148_084', '14_131', '157_197', '157_283', '157_368', ' 164_003', '164_022', '164_024', '166_054', '16_026', '16_029', '16_161', '16_186', '16_188', '16_190', '199_018', '210_0 46', '210_079', '216_056', '216_057', '216_058', '216_059', '216_060', '216_061', '216_077', '223_104', '223_105', '223_ 106', '223_108', '223_109', '238_043', '238_045', '238_046', '238_047', '251_048', '259_083', '259_084', '270_112', '270 _118', '270_126', '270_128', '32_058', '32_062', '32_063', '32_069', '32_109', '32_120', '37_045', '37_197', '44_004', ' 52_079', '53_060', '53_067', '53_095', '53_096', '53_097', '53_098', '53_114', '53_118', '53_144', '53_145', '53_174', ' 53_175', '53_176', '53_202', '53_206', '53_216', '53_217', '53_220', '53_240', '53_243', '53_244', '53_245', '53_246', ' 53_264', '53_266', '54_086', '54_088', '70_040', '70_041', '70_053', '70_076', '70_079', '70_081', '70_085', '70_097', ' 70_098', '70_126', '70_127', '70_128', '70_137', '70_138', '70_139', '70_144', '70_145', '70_173', '70_174', '70_175', ' 70_191', '70_192', '70_198', '70_220', '70_222', '70_223', '97_093', '97_124', '97_126', '97_127']

org_txt_path = './yolo_behavior_Dataset_all2/labels/val'
org_image_path = './yolo_behavior_Dataset_all2/images/val'

mv_txt_path = './filter/labels/val'
mv_image_path = './filter/images/val'

for file in specific_overlap_files:
    org_txt_file_path = os.path.join(org_txt_path, file+'.txt')
    org_image_file_path = os.path.join(org_image_path, file+'.jpg')

    mv_txt_file_path = os.path.join(mv_txt_path, file+'.txt')
    mv_image_file_path = os.path.join(mv_image_path, file+'.jpg')

    # 判断路径是否存在
    if os.path.exists(org_txt_file_path):
        # 移动文件
        shutil.move(org_txt_file_path, mv_txt_file_path)
        print(f"移动 {file} 到 {mv_txt_file_path}")
        
    if os.path.exists(org_image_file_path):
        # 移动文件
        shutil.move(org_image_file_path, mv_image_file_path)
        print(f"移动 {file} 到 {mv_image_file_path}")
        