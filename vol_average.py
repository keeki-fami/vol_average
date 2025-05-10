from pydub import AudioSegment
import os

#ファイルのwav変換と出力用ファイルの名前決めを行う
def exchange_file(base_file):
    p_base_file = base_file.replace("\"","")
    
    f_format = p_base_file.split('.')#ファイル名と拡張子に分けられるはず
    print(f_format)#確認用
    
    wav_file = f_format[0]+"_ave.wav"
    
    try:
        temp = AudioSegment.from_file(p_base_file,format=f_format[1])
        output_file = f_format[0]+".wav"
        print(output_file)
        temp.export(output_file,format='wav')
        
        return (wav_file,output_file)
    except Exception as e:
        print(f"エラーが発生しました。:{e}")
    
    

data = []
after_file = []
#ファイルの読み込み
while True:
    
    law_stdin = input().replace('\\','/') #ファイルのパスを標準入力する。
    stdin = law_stdin.replace("\"","")#加工する
    
    #ループ脱出用
    if(stdin=='0'):
        break
    else:
        wav_file,output_file = exchange_file(law_stdin)
        
        after_file.append(wav_file)#出力用ファイルを記録
        data.append(AudioSegment.from_wav(output_file))#wavに変換したファイルをdataに追加

      
#ファイルの詳細、追加されているファイル数、それぞれの音の大きさを出力
print("ファイル")
print(data)
print("ファイルの数:",len(data))
print("音量の大きさ")

loud = 0
for l in data:
    print(l.rms)
for i in data:
    loud += i.rms

loud_ave = loud//len(data)
print(loud//len(data))#平均を取る

change = []#音量の変更する量
for l in data:
    #各音声ファイルの変更する量をリストアップする
    change.append(loud_ave - l.rms)

print(change)#一応出力

data_ave = []
for index in range(len(data)):
    data_ave.append(data[index] + 0.00078*change[index])

print(data_ave)
#変更後の音量の大きさを出力
for i in data_ave:
    print(i.rms)

count=0
for music in data:
    new_file = after_file[count]
    #(おそらく)出力用ファイルは作られていないので、ここで作成する。
    if not os.path.exists(new_file):
        with open(new_file,'w')as file:
            file.write("あ")
        print(new_file,"を作成しました　。")
        print(new_file,"への書き込みを実行します。")
    
    else:
        print(new_file,"への書き込みを実行します。")
    
    music.export(new_file , format=new_file.split(".")[-1])
    print(new_file,"への書き込みが完了しました。")
    count+=1
