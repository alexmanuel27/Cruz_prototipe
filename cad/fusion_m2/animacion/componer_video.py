"""Add assembly instructions to actual Fusion frames, then encode a silent MP4.
Uses Pillow and the imageio-ffmpeg binary; does not control any desktop app.
"""
from pathlib import Path
import json, sys, subprocess, textwrap, tempfile
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'/tmp/cruz-animation-deps')
import imageio_ffmpeg
HERE=Path(__file__).resolve().parent
PLAN=json.loads((HERE/'PLAN_MONTAJE.json').read_text(encoding='utf-8'))
OUT=HERE/'rotulados';OUT.mkdir(exist_ok=True)
FONTS=Path('/System/Library/Fonts/Supplemental')
def font(size,bold=False):return ImageFont.truetype(str(FONTS/('Arial Bold.ttf' if bold else 'Arial.ttf')),size)
W,H=1920,1080
navy='#102B3B';teal='#1D7D83';muted='#4A6070'
def wrap(draw,text,f,width):
    lines=[];line=''
    for word in text.split():
        test=(line+' '+word).strip()
        if draw.textlength(test,font=f)>width and line:lines.append(line);line=word
        else:line=test
    if line:lines.append(line)
    return lines

def composite(idx,title,note,number=None):
    im=Image.new('RGB',(W,H),'#FFFFFF');d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,108),fill=navy)
    eyebrow='MONTAJE DEL INSTRUMENTO  /  FUSION CAD'
    d.text((32,15),eyebrow,font=font(21,True),fill='#9DCCD0')
    assert d.textlength(title,font=font(40,True))<1660,title
    assert len(wrap(d,note,font(27),1856))<=2,note
    d.text((32,45),title,font=font(40,True),fill='white')
    if number:d.text((1740,19),f'{number:02d} / {len(PLAN["steps"]):02d}',font=font(24,True),fill='white')
    view=Image.open(HERE/'frames'/f'{idx:04d}.png').convert('RGB')
    assert view.size==(1920,864)
    im.paste(view,(0,108))
    d=ImageDraw.Draw(im);d.rectangle((0,972,W,H),fill='#F0F5F6')
    for i,line in enumerate(wrap(d,note,font(27),1856)):
        d.text((32,985+32*i),line,font=font(27),fill=navy)
    d.rectangle((0,H-8,W,H),fill='#D7E4E7')
    if number:d.rectangle((0,H-8,int(W*number/len(PLAN['steps'])),H),fill=teal)
    path=OUT/f'{idx:04d}.png';im.save(path)
    return path

def main():
    missing=[i for i in range(PLAN['frame_count']) if not (HERE/'frames'/f'{i:04d}.png').exists()]
    assert not missing,f'{len(missing)} Fusion frames missing; first {missing[:5]}'
    intro=composite(0,'Secuencia de montaje del equipo','Orden de trabajo propuesto para el modelo actual. Revisar fijaciones y accesos con las piezas reales; PCB V8 todavía de estudio.')
    entries=[(intro,3)];clock=3.0;chapters=[]
    for s in PLAN['steps']:
        chapters.append({'step':s['number'],'start_seconds':round(clock,3),'title':s['title'],'note':s['note']})
        for i in range(s['render_count']):
            idx=s['first_frame']+i
            path=OUT/f'{idx:04d}.png'
            if '--reuse-captioned-frames' not in sys.argv:path=composite(idx,s['title'],s['note'],s['number'])
            assert path.exists()
            duration=1/PLAN['fps_render'] if s['moves'] else 0
            if i==s['render_count']-1:duration+=s['hold_seconds']
            assert duration>0
            entries.append((path,duration));clock+=duration
    concat=['ffconcat version 1.0']
    for path,duration in entries:
        # Paths are generated locally and contain no apostrophes.
        concat.extend([f"file '{path}'",f'duration {duration:.9f}'])
    concat.append(f"file '{entries[-1][0]}'")
    timeline=HERE/'timeline.ffconcat';timeline.write_text('\n'.join(concat)+'\n')
    metadata=[';FFMETADATA1','title=Instrument assembly — Cross M2','comment=Assembly order from the Fusion CAD model; proposed mechanical revision.']
    metadata.extend(['[CHAPTER]','TIMEBASE=1/1000','START=0','END=3000','title=00. Vista general'])
    for k,ch in enumerate(chapters):
        end=chapters[k+1]['start_seconds'] if k+1<len(chapters) else clock
        metadata.extend(['[CHAPTER]','TIMEBASE=1/1000',f"START={round(ch['start_seconds']*1000)}",f'END={round(end*1000)}',f"title={ch['step']:02d}. {ch['title']}"])
    chapter_file=HERE/'chapters.ffmetadata';chapter_file.write_text('\n'.join(metadata)+'\n',encoding='utf-8')
    ff=imageio_ffmpeg.get_ffmpeg_exe();output=HERE/'CROSS_MONTAJE_ORDEN_REAL_2026-11-03.mp4'
    # Image2 at 24 fps gives exact frame timing, including all reading pauses.
    # Symlinks live in a temporary folder rather than duplicating PNGs in the repo.
    with tempfile.TemporaryDirectory(prefix='cruz-assembly-video-') as folder:
        cumulative=0.;frame_index=0
        for path,duration in entries:
            cumulative+=duration;end_frame=round(cumulative*24)
            for n in range(frame_index,end_frame):
                (Path(folder)/f'{n:05d}.png').symlink_to(path)
            frame_index=end_frame
        subprocess.run([ff,'-y','-v','warning','-framerate','24','-start_number','0','-i',str(Path(folder)/'%05d.png'),'-f','ffmetadata','-i',str(chapter_file),'-map_metadata','1','-map_chapters','1','-r','24','-c:v','libx264','-threads','2','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(output)],check=True)

    (HERE/'CAPITULOS.json').write_text(json.dumps({'duration_seconds':round(clock,3),'chapters':chapters},ensure_ascii=True,indent=2)+'\n')
    # Poster and an overview sheet allow reviewing sequence without playing the video.
    Image.open(intro).save(HERE/'PORTADA_MONTAJE.png')
    sheet=Image.new('RGB',(1280,((len(PLAN['steps'])+4)//5)*214),'white');dr=ImageDraw.Draw(sheet)
    for s in PLAN['steps']:
        n=s['number']-1;x=(n%5)*256;y=(n//5)*214
        im=Image.open(OUT/f"{s['first_frame']+s['render_count']-1:04d}.png").crop((0,108,1920,972)).resize((256,115))
        sheet.paste(im,(x,y+14));dr.text((x+7,y+147),f"{s['number']:02d}",font=font(14,True),fill=teal)
        for j,line in enumerate(wrap(dr,s['title'],font(13),218)[:3]):dr.text((x+31,y+147+16*j),line,font=font(13),fill=navy)
    sheet.save(HERE/'SECUENCIA_MONTAJE.png')
    assert output.stat().st_size>100000
    print(json.dumps({'video':str(output),'duration_seconds':round(clock,3),'bytes':output.stat().st_size,'steps':len(chapters)}))
if __name__=='__main__':main()
