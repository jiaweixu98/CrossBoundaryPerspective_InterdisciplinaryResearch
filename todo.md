MAG中有大小journal共十余万个：124064。有一些非常脏，所以我们去看，jcr中的期刊有多少可以在MAG中找到。


JCR 2023 report:
我们匹配到JCR的数据，共匹配到13762本期刊，共14980本（91.8%）。可能MAG数据不全？有一些jcr期刊没有收录（可能是时间原因）。

我们必须考虑：第一作者的作用。

强条件：第一作者、末位作者。注意：经济学

我想得到这样一个结论：新的时代，尽管知识越来越专深（整体来讲，大家都很developed）。但跨界越来越容易了（我们更容易看到一些diversity的背景），可能是因为信息获取越来越便利。信息时代，科学越来越扁平，影响力上可能存在马太效应，但认知能力上则不是马太效应。一旦一个东西开源，拥有基本科学素养的人，只要采取合适的方法，付出足够的时间。未来科学界最重要的能力：发现好的研究问题。具备科学素养。勤奋。

证明的办法：跨界越来越常见了。跨界的效果还挺不错的。

D指标：我认为小团队更“自由”，在进行一种比较“新”的研究。D值大和小，倒也没有明显的好坏之分。

SCIE, SSCI, AHCI

SCIE & SSCI: 7类 'SUBSTANCE ABUSE', 'HISTORY & PHILOSOPHY OF SCIENCE', 'PUBLIC, ENVIRONMENTAL & OCCUPATIONAL HEALTH', 'NURSING', 'REHABILITATION', 'PSYCHIATRY', 'GREEN & SUSTAINABLE SCIENCE & TECHNOLOGY'

SSCI & AHCI: 3类 'HISTORY', 'CULTURAL STUDIES', 'HISTORY & PHILOSOPHY OF SCIENCE'

SSCI & SCIE: 1类 HISTORY & PHILOSOPHY OF SCIENCE

结论: JCR的不同索引下(例如SCIE, SSCI, AHCI), 其category是几乎等同的. 即 对于某一category(例如 HISTORY & PHILOSOPHY OF SCIENCE, 几乎所有被归到这一类的期刊,也同时被归属到SCIE, SSCI, AHCI三个索引中)



MAG data
参考MAG官方说明：Microsoft Academic Graph: When experts are not enough, 深入理解这个我们极为常用的数据，也是本文的重要数据。
Bootstrap不一定非得用，从较小的样本推总体的时候有用，如果已经是超大的样本，bootstrap的意义似乎不是很大。（主要是特别慢）

问题：
KeyInitialSetCounter：空的如何解决？
很难说，学科间转换的关系。因为一些学科间的转换本身就比较正常。因此我要做粒度更大的划分。
在测试