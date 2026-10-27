# MASS-OEF — Ontology Engineering Framework for MASS

**Governance status:** ADOPTED as methodological foundation  
**Adoption date:** 2026-10-27  
**Source:** `Ontology Engineering Framework for MASS (1).md` (user-provided research document)  
**Role:** project-wide engineering methodology; implemented incrementally under approved MASS Ontology Roadmap v1.1  
**Boundary:** adoption is not verification of all bibliography/normative claims or implementation of individual OWL modules. Applicable standards and IRIs must be independently reviewed and version-pinned before operative use.

> **Editorial note:** The source contained a long exported visualization/style string in section 5. In this repository-ready copy it is represented by a readable Mermaid diagram preserving the visible architecture labels. The substantive text, tables and cited sources are otherwise retained. The source file remains the archival reference.

---

							

## **Вывод**

Полного аналога `\`, который одновременно охватывал бы нормативную модель, системную архитектуру, эксплуатацию, безопасность, береговое управление и данные жизненного цикла, не обнаружено. Существующие работы покрывают отдельные части такого framework:

* архитектуру автономной навигации;  
* системную инженерию автономного судна;  
* онтологическую инфраструктуру судовых подсистем;  
* ситуационную осведомлённость;  
* safety assurance;  
* цифровой двойник;  
* стандартизацию MASS.

Приложенный Ontology\_Engineering\_Framework\_for\_Space\_Systems\_Data\_Repository.pdf, DOI: [10.1109/ACCESS.2026.3676643](https://doi.org/10.1109/ACCESS.2026.3676643), можно использовать как методологическое основание, но его ядро необходимо изменить с `SystemElement-centric` на `socio-technical operational system-centric`.

## **1\. Ближайшие работы**

### **Архитектура MASS**

Наиболее полную функциональную декомпозицию автономной навигации дают Alamoush и Ölçer. Framework включает семь кластеров: архитектуру автономной навигации, принятие решений, ситуационную осведомлённость, sensor fusion, collision avoidance, управление движением, швартовку \[1\].

[Maritime Autonomous Surface Ships: Architecture for Autonomous Navigation Systems](https://consensus.app/papers/maritime-autonomous-surface-ships-architecture-for-alamoush-%C3%B6l%C3%A7er/63308d61ea7056449cf0aa4bf07ce3b8/?utm_source=chatgpt) — A. S. Alamoush, A. Ölçer, 2025, *Journal of Marine Science and Engineering*, цитирований в Consensus: 44\. DOI: [10.3390/jmse13010122](https://doi.org/10.3390/jmse13010122).

Использование: источник функциональных модулей и первичных competency questions, но не готовая онтология.

### **Systems Engineering framework**

Dittmann рассматривает автономное судно как киберфизическую систему, состоящую из vendor-specific аппаратных и программных компонентов. Архитектура включает безопасное поведение, выявление неспособности автономной системы продолжать операцию и запрос вмешательства человека. Подход проверен на проекте GreenHopper \[2\].

[Autonomy for Ships: System Thinking and Engineering](https://consensus.app/papers/autonomy-for-ships-system-thinking-and-engineering-dittmann/c1c80177f26854f2a0ace5ff66bdaaf4/?utm_source=chatgpt) — K. Dittmann, 2022, *SoftCOM 2022*, с. 1–6, цитирований: 3\. DOI: [10.23919/SoftCOM55329.2022.9911446](https://doi.org/10.23919/SoftCOM55329.2022.9911446).

Использование: определения `AutonomousFunction`, `Fallback`, `HumanInterventionRequest`, `OperationalLimitation`, `DegradedMode`.

### **Онтологическая инфраструктура автономного судна**

Sumić et al. предлагают онтологическую информационную инфраструктуру для обеспечения совместимости интеллектуальных агентов. Пример реализован для противопожарной системы автономного судна \[3\].

[Ontology-Based Information Infrastructure for Autonomous Ships](https://consensus.app/papers/ontologybased-information-infrastructure-for-sumi%C4%87-male%C5%A1/d5b133c3802c5fa58ee4b64db149702f/?utm_source=chatgpt) — D. Sumić, L. Maleš, T. Marušić, M. Rosić, 2024, *Transactions on Maritime Science*, цитирований: 2\. DOI: [10.7225/toms.v13.n01.008](https://doi.org/10.7225/toms.v13.n01.008).

Это ближайший аналог эксплуатационной части OEF, но область ограничена отдельной судовой системой.

### **Распределённая ситуационная осведомлённость**

Song et al. объединяют в онтологии знания MASS, пилотируемого судна, VTS, Remote Control Centre и береговых служб. SWRL применяется для обнаружения противоречий между индивидуальной и authority-based situational awareness \[4\].

[Distributed Situational Awareness for Maritime Autonomous Surface Ships in Mixed Waterborne Transport: An Ontology-based Framework](https://consensus.app/papers/distributed-situational-awareness-for-maritime-song-papadimitriou/f02b380dd04f532dbb237ddfd668e6af/?utm_source=chatgpt) — R. Song, E. Papadimitriou, R. Negenborn, P. van Gelder, 2023, *ICTIS 2023*, с. 1088–1092, цитирований: 4\. DOI: [10.1109/ICTIS60134.2023.10243802](https://doi.org/10.1109/ICTIS60134.2023.10243802).

Использование: модель распределённых ролей, полномочий, наблюдений и конфликтующих представлений ситуации.

### **Safety assurance framework**

Nakashima et al. объединяют MBSE, STPA, FMEA и simulation-based verification. Существенное достоинство — прослеживаемость от safety goal и loss scenario до требований, проектных решений и результатов испытаний \[5\].

[Towards Integrated Safety Assurance Methodology for Autonomous Vessel Navigation Systems](https://consensus.app/papers/towards-integrated-safety-assurance-methodology-for-nakashima-kureta/a87195dc68825b7a9f7fc29b6d71c5d0/?utm_source=chatgpt) — T. Nakashima, R. Kureta, J. Nakamura, 2024, *Journal of Physics: Conference Series*, том 2867, цитирований: 3\. DOI: [10.1088/1742-6596/2867/1/012038](https://doi.org/10.1088/1742-6596/2867/1/012038).

Это наиболее подходящий источник для расширения исходных Ontology Design Rules до формальной модели safety assurance.

Wylie и Rajabally дополняют подход goal-based compliance, EMSA Risk Based Assessment Tool и традиционными методами оценки риска \[6\].

[Safety Assurance of Maritime Autonomous Surface Ships](https://consensus.app/papers/safety-assurance-of-maritime-autonomous-surface-ships-wylie-rajabally/c81428bd39c1515ca01e7254f3b74271/?utm_source=chatgpt) — M. Wylie, E. Rajabally, 2024, *Journal of Physics: Conference Series*, том 2867, цитирований: 4\. DOI: [10.1088/1742-6596/2867/1/012045](https://doi.org/10.1088/1742-6596/2867/1/012045).

### **Системная структура для hazard analysis**

Chaal et al. строят иерархическую модель автономного судна на основе системной теории и STCW. Функции экипажа либо передаются технической системе, либо назначаются Shore Control Centre \[7\].

[An Initial Hierarchical Systems Structure for Systemic Hazard Analysis of Autonomous Ships](https://consensus.app/papers/an-initial-hierarchical-systems-structure-for-systemic-chaal-banda/b9cfbbb3cf6f509cbd55d6c7eccdfbb1/?utm_source=chatgpt) — M. Chaal, O. Valdez Banda, S. Basnet, S. Hirdaris, P. Kujala, 2020, *ISSAV/European STAMP Conference*, цитирований: 9\.

Использование: формализация отношений `performsFunction`, `replacesCrewFunction`, `assignedToROC`, `controls`, `supervises`.

### **Digital Twin framework**

Menges и Rasheed предлагают шесть уровней зрелости цифрового двойника ASV: standalone, descriptive, diagnostic, predictive, prescriptive и autonomous \[8\].

[Digital Twin for Autonomous Surface Vessels: Enabler for Safe Maritime Navigation](https://consensus.app/papers/digital-twin-for-autonomous-surface-vessels-enabler-for-menges-rasheed/34c047a9d4935cdc861b9107d537d5ee/?utm_source=chatgpt) — D. Menges, A. Rasheed, 2024, *arXiv abs/2411.03465*, цитирований: 8\.

Использование: эксплуатационный и runtime-слой, но не источник нормативной семантики.

MontoFlow и SHIP Ontology дают готовую модель сенсоров, судовых компонентов, наблюдений, пороговых значений и аномалий на основе SSN/SOSA \[9\].

[MontoFlow — A Maritime Ontology Framework for Modeling Ship Sensory Systems](https://consensus.app/papers/montoflow-a-maritime-ontology-framework-for-modeling-ship-ivanovic-burbach/58ec885ce4f35f779b13111a99525d63/?utm_source=chatgpt) — P. Ivanovic, S. Burbach, M. Maleshkova, 2025, с. 276–294, цитирований: 1\. DOI ресурса: [10.5281/zenodo.15390282](https://doi.org/10.5281/zenodo.15390282).

## **2\. Нормативная основа MASS-OEF**

В исходном OEF роль нормативного ядра выполняют ECSS-E-TM-10-23A и связанные стандарты. Для MASS таким ядром теперь должен быть International Code of Safety for MASS.

IMO приняла первый необязательный MASS Code 22 мая 2026 года; он применяется с 1 июля 2026 года. Код построен как goal-based framework и охватывает risk assessment, operational context, system design, software principles, управление безопасностью, навигацию, connectivity, remote operations, пожарную безопасность, search and rescue, machinery и другие области. Обязательный код планируется принять к 1 июля 2030 года с вступлением в силу в 2032 году. [Официальное сообщение IMO](https://www.imo.org/en/mediacentre/pressbriefings/pages/imo-adopts-mass-code.aspx?utm_source=chatgpt.com).

Нормативный корпус MASS-OEF:

| Уровень | Источники |
| ----- | ----- |
| Базовый международный | MASS Code, SOLAS, COLREG, MARPOL, STCW, SAR Convention, FAL Convention |
| Управление безопасностью | ISM Code, Formal Safety Assessment, EMSA RBAT |
| Кибербезопасность | IMO cyber-risk guidance, IEC 62443, IACS UR E26/E27 |
| Навигационная информация | IMO e-Navigation, IHO S-100, IALA S-200, IEC 61162 |
| Автономные функции | ISO/TS 23860:2022, ISO/TC 8/SC 26 проекты |
| Классификация | правила DNV, LR, ABS, BV, RINA для autonomous and remotely operated ships |
| Организационный уровень | Safety Management System оператора, процедуры ROC, проектные ограничения |

ISO/TS 23860:2022 уже задаёт терминологию autonomous ship systems. Разрабатываемый ISO/AWI 25922 должен описывать способности MASS и распределение ответственности между автоматикой и людьми. Это делает их прямыми источниками терминов и competency questions для онтологии: [ISO/TS 23860](https://www.iso.org/standard/77186.html?utm_source=chatgpt.com), [ISO/AWI 25922](https://www.iso.org/standard/92067.html?utm_source=chatgpt.com).

## **3\. Что можно перенести из OEF без изменений**

| Компонент исходного OEF | Решение для MASS |
| ----- | ----- |
| Ontology as system requirement | MASS ontology становится обязательной концептуальной схемой обмена проектными и эксплуатационными данными |
| Information-sharing driven | В онтологию включается понятие, если оно требуется другому участнику жизненного цикла или safety process |
| Tool independence | OWL/RDF как нейтральный уровень между SysML, судовыми системами, ROC и цифровым двойником |
| Modularity | Отдельные ортогональные модули по функциям, безопасности, операциям и данным |
| Competency questions | CQs используются как формальные требования к каждому модулю |
| Ontology Design Rules | Нормативные и инженерные правила реализуются через SWRL, SHACL и специализированные rule engines |
| Continuous validation | Итерационная проверка на реальных данных, симуляциях и испытаниях |
| Linked Data | Связывание распределённых проектных, судовых и береговых репозиториев |
| Configuration control | Версионирование онтологий, dataset versions, provenance и approvals |
| FAIR/open ontology | Открытое ядро и контролируемые проектные расширения |

## **4\. Что необходимо изменить**

### **4.1. Заменить центральный класс**

В космическом OEF центральным понятием является `SystemElement`, к которому привязываются требования, функции, компоненты и результаты испытаний.

Для MASS этого недостаточно. Предлагаемое ядро:

MASSOperation  
  involves Vessel  
  occursWithin OperationalContext  
  isPerformedBy AutonomousFunction / HumanAgent  
  isSupervisedBy ROC  
  isConstrainedBy Regulation  
  produces OperationalState  
  encounters Hazard  
  isSupportedBy Evidence

Центральной единицей интеграции должен стать не физический компонент, а `OperationalConfiguration`:

\\\[ OC \= \\langle Vessel,\\ AutonomyMode,\\ FunctionAllocation,\\ ODD,\\ HumanOversight,\\ Connectivity,\\ ApplicableRules \\rangle \\\]

Именно конфигурация определяет, кто выполняет функцию, какие правила применимы и какие доказательства безопасности необходимы.

### **4.2. Ввести Operational Design Domain**

OEF для космических систем ориентирован преимущественно на жизненный цикл изделия. Для MASS необходимо формально представить область допустимой эксплуатации:

* географическую область;  
* тип водного пути;  
* видимость;  
* ветер, волнение и течение;  
* интенсивность движения;  
* состав окружающих участников;  
* доступность GNSS и связи;  
* уровень картографического и гидрографического обеспечения;  
* допустимые режимы автономности;  
* границы перехода в degraded/fallback state.

Основное ограничение:

AutonomousFunction mayOperate onlyIf  
CurrentOperationalContext conformsTo ApprovedODD

### **4.3. Представить динамическое распределение функций**

Функции переходят между:

* экипажем на борту;  
* автономной системой;  
* remote operator;  
* ROC supervisor;  
* внешней службой VTS.

Поэтому отношение `performsFunction` должно быть временным и контекстным:

FunctionAllocation  
  allocates Function  
  to Agent  
  during TimeInterval  
  under OperationalContext  
  with AuthorityLevel

Это позволит описывать handover, takeover, loss of communication и возврат к автономному режиму.

### **4.4. Отделить требования от применимости**

Для MASS нельзя считать каждое нормативное требование универсально применимым. Применимость зависит от типа судна, режима автономности, рейса, района плавания и наличия людей на борту.

Необходима конструкция:

RegulatoryRequirement  
  hasApplicabilityCondition  
  appliesTo OperationalConfiguration  
  isSatisfiedBy Evidence

Это превращает онтологию одновременно в:

* модель нормативных требований;  
* механизм applicability analysis;  
* основу compliance matrix;  
* источник safety case.

### **4.5. Расширить Ontology Design Rules**

В исходной работе ODR подразделяются по источникам и эффектам. Для MASS целесообразны пять групп:

1. `Regulatory rules`: MASS Code, SOLAS, COLREG, STCW.  
2. `Safety rules`: STPA constraints, FMEA mitigations, risk controls.  
3. `Operational rules`: ODD, route, traffic, weather, port restrictions.  
4. `Organizational rules`: полномочия master, ROC и remote operator.  
5. `Technical rules`: sensor coverage, redundancy, connectivity, latency.

По эффекту:

* классификация ситуации;  
* выявление несоответствия;  
* вывод применимого требования;  
* формирование предупреждения;  
* инициирование fallback;  
* построение compliance report;  
* формирование safety-case evidence chain.

Критические действия не следует непосредственно исполнять через SWRL. Онтология должна выводить рекомендацию или выявлять нарушение; управление судном должно оставаться в сертифицированном runtime-контуре.

## **5\. Предлагаемая архитектура MASS-OEF**

```mermaid
flowchart TD
    REG["Нормативное ядро: MASS Code, SOLAS, COLREG"]
    CORE["MASS Core Ontology"]
    DESIGN["Проектные модули: системы, функции, ПО"]
    OPS["Операционные модули: ODD, voyage, ROC, VTS"]
    ASSURANCE["Assurance-модули: hazard, risk, evidence"]
    KG["Federated MASS Knowledge Graph"]
    VALID["Проверка: SHACL, rules, reasoning"]
    APPS["MBSE, Digital Twin, ROC, compliance reports"]
    REG --> CORE
    CORE --> DESIGN
    CORE --> OPS
    CORE --> ASSURANCE
    DESIGN --> KG
    OPS --> KG
    ASSURANCE --> KG
    KG --> VALID
    VALID --> APPS
```

Рекомендуемые модули:

| Модуль | Основные понятия |
| ----- | ----- |
| `MASS-Core` | System, SystemElement, Function, Capability, Interface |
| `MASS-Vessel` | Vessel, ShipSystem, Propulsion, Steering, Power, FireSafety |
| `MASS-Autonomy` | AutonomousFunction, AutonomyMode, Decision, Action, Fallback |
| `MASS-Human` | Master, Crew, RemoteOperator, ROCSupervisor, Authority |
| `MASS-Operations` | Voyage, Mission, OperationalConfiguration, Handover |
| `MASS-ODD` | GeographicArea, Weather, Visibility, Traffic, Connectivity |
| `MASS-Navigation` | Route, Encounter, Manoeuvre, CollisionRisk, COLREGRole |
| `MASS-Situation` | Observation, Object, Event, Situation, Uncertainty |
| `MASS-Sensors` | Sensor, Observation, Accuracy, Coverage, Failure; переиспользование SSN/SOSA и SHIP |
| `MASS-Communication` | Link, Channel, Message, Latency, Availability, CyberState |
| `MASS-ROC` | RemoteOperation, Supervision, Intervention, HandoverRequest |
| `MASS-Safety` | Hazard, Loss, SafetyConstraint, RiskControl, SafeState |
| `MASS-Regulation` | Instrument, Requirement, Applicability, ComplianceStatus |
| `MASS-Assurance` | Claim, Argument, Evidence, VerificationResult, Provenance |
| `MASS-Lifecycle` | DesignVersion, SoftwareVersion, Configuration, Maintenance |
| `MASS-DigitalTwin` | PhysicalAsset, DigitalRepresentation, StateUpdate, Simulation |

## **6\. Адаптированный процесс разработки**

### **Шаг 1\. Определить scope через operational use cases**

Первый модуль не должен охватывать «всё автономное судно». Практичный scope:

> Семантическая интеграция данных автономной навигации, ROC и safety assurance для одного типа MASS в ограниченном ODD.

Участники:

* ship designer;  
* autonomy-system supplier;  
* shipowner/operator;  
* ROC operator;  
* master;  
* classification society;  
* flag state;  
* port/VTS;  
* maritime university;  
* ontology engineer.

### **Шаг 2\. Сформировать competency questions**

Минимальный набор:

1. Какой агент отвечает за конкретную функцию в текущем режиме?  
2. Допустим ли текущий режим автономности в данных условиях?  
3. Какие требования MASS Code применимы к этой конфигурации?  
4. Какие сенсоры обеспечивают конкретное safety-critical решение?  
5. Достаточна ли их точность, доступность и область покрытия?  
6. Какие функции становятся недоступными при потере связи с ROC?  
7. Какое fallback-состояние требуется при конкретном отказе?  
8. Кто обладает authority инициировать handover?  
9. Какие опасности связаны с данным решением автономной системы?  
10. Какими результатами испытаний подтверждено safety requirement?  
11. Какая версия ПО использовалась при получении evidence?  
12. Выполняются ли COLREG-ограничения в конкретном encounter?  
13. Противоречат ли представления ситуации MASS, ROC и VTS?  
14. Соответствует ли текущая эксплуатационная обстановка ODD?  
15. Какие изменения конструкции инвалидируют существующий safety case?

### **Шаг 3\. Извлечь ключевые термины**

Источники обрабатываются раздельно:

* нормативные документы;  
* архитектурные модели SysML;  
* STPA/FMEA;  
* эксплуатационные процедуры;  
* sensor/interface specifications;  
* ROC procedures;  
* incident and near-miss reports;  
* AIS, radar, ECDIS и simulator datasets.

Для каждого термина фиксируются:

* нормативный источник;  
* определение;  
* контекст применимости;  
* синонимы;  
* владелец;  
* версия;  
* связь с competency question.

### **Шаг 4\. Выполнить reuse assessment**

Переиспользовать:

* BFO или иной верхний уровень;  
* Common Core Ontologies — роли, агенты, процессы;  
* W3C SSN/SOSA — сенсоры и наблюдения;  
* QUDT — величины и единицы;  
* OWL-Time — временные отношения;  
* GeoSPARQL — география и районы;  
* PROV-O — происхождение evidence;  
* SHIP Ontology — судовые сенсоры и компоненты.

Не импортировать внешнюю онтологию целиком без проверки границ, лицензии, устойчивости URI и совместимости с нормативной семантикой.

### **Шаг 5\. Построить conceptualization cycle**

В отличие от исходного OEF, следует параллельно развивать четыре представления:

1. `Structural`: судно, ROC, системы и интерфейсы.  
2. `Functional`: функции и их распределение между людьми и автоматикой.  
3. `Operational`: ODD, voyage, режимы и ситуации.  
4. `Assurance`: hazards, requirements, evidence и compliance.

Каждый новый класс должен:

* иметь верхний класс;  
* иметь текстовое определение;  
* быть связан с CQ;  
* иметь владельца;  
* иметь источник;  
* не дублировать существующий модуль;  
* иметь ожидаемый пример instance data.

### **Шаг 6\. Формализовать правила и ограничения**

Распределение технологий:

| Задача | Технология |
| ----- | ----- |
| Семантическая классификация | OWL 2 DL |
| Ограничения данных | SHACL |
| Дополнительный вывод | SWRL или N3 rules |
| Запросы | SPARQL |
| Provenance | PROV-O и named graphs |
| Safety-case structure | SACM-подобная модель или отдельная assurance ontology |
| Версии | Git \+ ontology release identifiers |
| Runtime events | event stream, связанный с knowledge graph через adapters |

### **Шаг 7\. Валидировать в трёх контурах**

**Онтологическая валидация**

* consistency reasoner;  
* отсутствие orphan classes;  
* отсутствие непреднамеренного overlap;  
* проверка domain/range;  
* OOPS/FOOPS-подобные quality checks.

**Информационная валидация**

* SHACL-проверка реальных datasets;  
* ответы на competency questions;  
* полнота mapping из SysML, AIS, sensor logs и ROC data;  
* round-trip transformation.

**Инженерная валидация**

* simulation-based scenarios;  
* hardware/software-in-the-loop;  
* ROC operator in the loop;  
* реальные испытания;  
* проверка traceability от hazard до evidence.

## **7\. Пилотный кейс**

Наиболее подходящий первый case study:

> Потеря связи MASS с ROC во время расхождения с пилотируемым судном в ограниченной видимости.

Он одновременно задействует:

* MASS Code;  
* COLREG;  
* автономную навигацию;  
* sensor fusion;  
* situational awareness;  
* connectivity;  
* ROC;  
* authority allocation;  
* fallback;  
* risk assessment;  
* verification evidence.

Ожидаемая цепочка:

LossOfConnectivity  
→ invalidates RemoteSupervisionCapability  
→ changes FunctionAllocation  
→ activates AutonomousFallbackMode  
→ requires MinimumRiskCondition  
→ constrainedBy COLREG  
→ verifiedBy SimulationScenario  
→ supportedBy TestEvidence

Критерий успешности пилота: knowledge graph автоматически определяет применимые требования, обнаруживает нарушение ODD или safety constraints, показывает ответственного агента и извлекает доказательства, подтверждающие допустимость fallback-решения.

## **8\. Основная научная новизна**

Адаптированный framework можно сформулировать как:

> MASS Ontology Engineering and Assurance Framework — модульный нормативно-ориентированный framework для семантической интеграции проектных, эксплуатационных и assurance-данных автономного судна, обеспечивающий контекстное распределение функций между человеком и автоматикой, автоматизированный анализ применимости требований и прослеживаемость от нормативной цели до эксплуатационного доказательства.

Отличие от найденных работ:

* от архитектурных frameworks — формальная машинно-интерпретируемая семантика;  
* от существующих морских онтологий — охват полного жизненного цикла;  
* от safety frameworks — единая модель требований, конструкции, эксплуатации и evidence;  
* от digital twins — нормативная применимость и assurance;  
* от исходного Space OEF — динамический ODD, распределённая ответственность и runtime safety.
