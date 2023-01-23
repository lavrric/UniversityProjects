%{
	#define YYDEBUG 1
%}

%token NUMBER
%token IN
%token OUT
%token ELIF
%token IF
%token ELSE
%token WHILE

%token OPEN_ROUND
%token CLOSE_ROUND
%token OPEN_CURLY
%token CLOSE_CURLY
%token ATTR
%token SEMICOLON

%token ID
%token INT_CONST
%token STRING_CONST

%token AND
%token LE
%token GE
%token EQ
%token NEQ

%left AND
%left '<' '>' GE LE EQ NEQ
%left '+' '-'
%left '*' '/'
%left '%'

%start program
%%
program: stmtList {printf("program -> stmtList\n");} ;
stmtList: stmt { printf("stmtList -> stmt\n"); }
	| stmtList stmt { printf("stmtList -> stmtList stmt\n"); }
	;
stmt: 	cmpdStmt { printf("stmt -> cmpdStmt\n"); }
	| ifStmt { printf("stmt -> ifStmt\n"); }
	| whileStmt { printf("stmt -> whileStmt\n"); }
	| outStmt { printf("stmt -> outStmt\n"); }
	| assignStmt { printf("stmt -> assignStmt\n"); };

cmpdStmt: OPEN_CURLY stmtList CLOSE_CURLY { printf("cmpdStmt -> { ... }\n"); };
ifStmt:   IF OPEN_ROUND exp CLOSE_ROUND stmt { printf("ifStmt -> if ..\n"); };
	| IF OPEN_ROUND exp CLOSE_ROUND stmt ifTail { printf("ifStmt -> if .. ifTail\n"); };
ifTail: ELIF OPEN_ROUND exp CLOSE_ROUND stmt { printf("ifTail -> elif ...\n"); }
	| ELIF OPEN_ROUND exp CLOSE_ROUND stmt ifTail { printf("ifTail -> elif ... + ifTail\n"); }
whileStmt: WHILE OPEN_ROUND exp CLOSE_ROUND stmt { printf("whileStmt -> while(...){}\n");};
assignStmt: ID ATTR exp SEMICOLON {printf("assignStmt -> ID = exp;\n");};
outStmt:  OUT OPEN_ROUND const CLOSE_ROUND SEMICOLON { printf("outStmt -> ...\n");}
	| OUT OPEN_ROUND ID CLOSE_ROUND SEMICOLON { printf("outStmt -> ...\n");}
	;
const: 	INT_CONST { printf("const -> INT_CONST\n");}
	| STRING_CONST { printf("const -> STRING_CONST\n");}
	;
exp: 	term { printf("exp -> term\n");}
	| exp op term { printf("exp -> exp op term\n");}
	| exp rel_op term { printf("exp -> exp rel_op term\n");}
	;
op: 	'+' | '-' | '*' | '/' | '%';
rel_op: AND | '>' | '<' | GE | LE | EQ | NEQ;
term: 	ID { printf("term -> ID\n");}
	| const { printf("term -> const\n");};
%%
yyerror(char *s)
{
	printf("%s\n",s);
}
extern FILE *yyin;

main(int argc, char **argv)
{
	if(argc>1) yyin = fopen(argv[1],"r");
	if(!yyparse()) fprintf(stderr, "\tOK\n");
}

