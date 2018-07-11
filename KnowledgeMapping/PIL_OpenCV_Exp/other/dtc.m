RGB=imread('timg.jpg');  %读取图像到RGB
RGB=imresize(RGB,[168,224]);                    %改变图像大小
imwrite(RGB,'start.jpg'); %将改变后的图像存入start.jpg

R=RGB(:,:,1);
G=RGB(:,:,2);
B=RGB(:,:,3);
figure,imshow(RGB),title('orgin');

%RGB->YUV
Y=0.299*double(R)+0.587*double(G)+0.114*double(B);
U=-0.169*double(R)-0.3316*double(G)+0.5*double(B);
V=0.5*double(R)-0.4186*double(G)-0.0813*double(B);
YUV=cat(3,Y,U,V);%YUV图像
figure,imshow(uint8(YUV)),title('YUV')

T=dctmtx(8);%产生一个8×8的DCI变换矩阵


%进行DCT变换 BY BU BV 是double类型
BY=blkproc(Y,[8 8],'P1*x*P2',T,T');
BU=blkproc(U,[8 8],'P1*x*P2',T,T');
BV=blkproc(V,[8 8],'P1*x*P2',T,T');

a=[16 11 10 16 24 40 51 61;
      12 12 14 19 26 58 60 55;
      14 13 16 24 40 57 69 55;
      14 17 22 29 51 87 80 62;
      18 22 37 56 68 109 103 77;
      24 35 55 64 81 104 113 92;
      49 64 78 87 103 121 120 101;
      72 92 95 98 112 100 103 99;]; %量化值

  b=[17 18 24 47 99 99 99 99;
      18 21 26 66 99 99 99 99;
      24 26 56 99 99 99 99 99;
      47 66 99 99 99 99 99 99;
      99 99 99 99 99 99 99 99;
      99 99 99 99 99 99 99 99;
      99 99 99 99 99 99 99 99;
      99 99 99 99 99 99 99 99;];

%BY2 BU2 BV2是double类型
BY2=blkproc(BY,[8 8],'x./P1',a);
BU2=blkproc(BU,[8 8],'x./P1',b);
BV2=blkproc(BV,[8 8],'x./P1',b);
%这里进行取整量化,BY3 BU3 BV3是uint8类型
BY3=int8(BY2);
BU3=int8(BU2);
BV3=int8(BV2);

%BY4 BU4 BV4是double类型
BY4=blkproc(double(BY3),[8 8],'x.*P1',a);
BU4=blkproc(double(BU3),[8 8],'x.*P1',b);
BV4=blkproc(double(BV3),[8 8],'x.*P1',b);

mask=[
      1 1 1  1 1 1 1 1;
      1 1 1  1 1 1 1 1;
      1 1 1  1 1 1 1 1;
      1 1 1  1 1 1 1 1;
      1 1 1  1 1 1 1 1;
      1 1 1  1 1 1 1 1;
      1 1 1  1 1 1 1 1;
      1 1 1  1 1 1 1 1;];
%BY5 BU5 BV5是double类型
BY5=blkproc(BY4,[8 8],'P1.*x',mask);
BU5=blkproc(BU4,[8 8],'P1.*x',mask);
BV5=blkproc(BV4,[8 8],'P1.*x',mask);

%YI UI VI是double类型
YI=blkproc(double(BY5),[8 8],'P1*x*P2',T',T);
UI=blkproc(double(BU5),[8 8],'P1*x*P2',T',T);
VI=blkproc(double(BV5),[8 8],'P1*x*P2',T',T);

%YUVI是double类型
YUVI=cat(3,uint8(YI),uint8(UI),uint8(VI));%经过DCT变换和量化后的YUV图像
figure,imshow(YUVI),title('DCT2YUV');

RI=YI-0.001*UI+1.402*VI;
GI=YI-0.344*UI-0.714*VI;
BI=YI+1.772*UI+0.001*VI;
RGBI=cat(3,RI,GI,BI);%经过DCT变换和量化后的RGB图像
RGBI=uint8(RGBI);
figure,imshow(RGBI),title('DCT2RGB');
imwrite(RGBI,'end.jpg'); %保存压缩图像