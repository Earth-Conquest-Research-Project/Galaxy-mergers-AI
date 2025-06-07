# 🌌MultimodalAI Model for Classifying Galaxy Mergers🌌 

🔭 캡스톤 스타트 : 우주정복 7팀 

![메인페이지](./readMe_image/mergeGalaxy.png)
<small> 이미지 출처 : Kurzgesagt – In a Nutshell </small>

<div style="border: 3px solid blue; padding: 10px; border-radius: 10px;">

## 연구 주제
<b> 은하 병합 여부를 분류하는 멀티모달 AI 모델 연구 개발 </b>
<br/><br/>
천문 시뮬레이션 데이터를 기반으로 은하 간 병합 여부(O/X)와 병합의 시간 단계(Pre-merger / Ongoing / Post-merger)를 예측할 수 있는 멀티모달 AI 분류 모델을 개발한다. 이를 위해 은하 이미지와 물리량(질량, 속도, 별 형성률 등)을 결합해 병합의 시간 단계를 자동으로 분류하고, 시계열적 병합 이력까지 추정할 수 있는 AI 기반 은하 병합 탐지 시스템을 구축한다.
<br/>
</div>

<br/>

## 기대 효과 및 발전 가능성
<b> 기대효과 </b><br/>
멀티모달 AI 기술을 활용해 대규모 관측 데이터에서 은하 충돌과 병합 사건을 자동으로 탐지함으로서 은하의 장기적 진화 양상을 이해하는데 기여한다.

<b> 추후 발전 가능성 </b><br/>
각 은하에 대해 충돌 시점, 동반 은하 후보, 충돌 횟수를 포함하는 시계열적 병합 이력 재구성을 통해 시간에 따른 유기적인 은하 진화 과정을 밝히는데 기여한다.

<br/>

## 성과
<!-- 성과 칸 -->
🏆 한국천문연구원 SpaceAI 2025 연구 과제 선정 <br/>
<br/>

## 연구 팀

### 🔭 우주정복 캡스톤 7팀
|                        이한나                     |                          정은채                      |                          정소은                        |
|:------------------------------------------------:|:---------------------------------------------------------:|:-------------------------------------------------:|
|             <img src="https://avatars.githubusercontent.com/u/89291223?s=400&u=64dcff931bf6efee8bb8cc371573472faa9b373f&v=4"/>             | <img src="https://avatars.githubusercontent.com/u/104445068?v=4"/> | <img src="https://avatars.githubusercontent.com/u/112189780?v=4"/> |
|                     [@hannah0226](https://github.com/hannah0226)                      |            [@Goldchae](https://github.com/Goldchae)            |            [@sunnism03](https://github.com/sunnism03)            |
| - |   -   |       -   |    

<br>
<br/>

### 🔭 SYENERGI ( 세종-연세-이화 은하 상호작용 연구 네트워크 )
|                        AI팀                    |                          천문학팀                      |
|:------------------------------------------------:|:---------------------------------------------------------:|
|                     이화여자대학교 컴퓨터공학전공                     |           연세대학교 천문우주학과, 세종대학교           |
| 이한나, 정은채, 정소은 |   지웅배교수님, 강희수 연구원님, 이예진 연구원님, 김은택 연구원님   |


<br/>
<br/>



## 연구 상세

### 🔭 아키텍처 
![아키텍처](https://github.com/user-attachments/assets/9f2bd3b1-9ddb-4d38-b199-30c8f3d6e34d)

### 🔭 데이터

TNG50-1 데이터

-  병합 은하(Merger): 
조건 : SnapNumLastMerger가 현재 snapshot 기준 0.5 Gyr 이내인 경우
개수 : - 개 

- 비병합 은하(Non-merger):
조건 : 병합 이력이 없거나 SnapNumLastMerger가 너무 오래 전인 경우
개수: - 개 

### 🔭 디렉토리 구조   
```
.
├── data   
│   ├── processed      # 모델 학습을 위해 전처리된 최종 데이터   
│   └── raw            # 원본 데이터
│
├── models             # 학습된 모델(pkl 등) 저장
│
├── notebooks          # 탐색적 분석, 실험용 노트북
│
├── src
│   ├── data           # 데이터를 로드, 클린징, 변환하는 스크립트
│   ├── feature        # 특징 추출 및 피처 엔지니어링 스크립트
│   └── models         # 모델 정의, 학습, 예측 관련 스크립트
```

<br/>
<br/>
<br/>


## 연구 진행 노트

<table style="width: 100%;  border: 3px solid Blue;  ">
  <tr>
    <td>
      <h3>v1.0.0 (2025-3-)</h3>
      <ul>
        <li><strong>아키텍처</strong>: late fusion, 물리량부 - MLP, 이미지부 - zoobot -  </li>
        <li><strong>데이터</strong>: 물리량 랜덤값 세팅 </li>
        <li><strong>기타</strong>: </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>
      <h3>v1.x.x (추후 업데이트 예정)</h3>
      <ul>
        <li><strong>개선한 사항</strong>: </li>
        <li><strong>최적화 내용</strong>: </li>
      </ul>
    </td>
  </tr>
</table>

