#include "algtest.h"
#include <QtWidgets/QApplication>

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	algtest w;
	w.show();
	return a.exec();
}