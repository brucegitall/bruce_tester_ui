#ifndef ALGTEST_H
#define ALGTEST_H

#include <QtWidgets/QMainWindow>
#include <QSignalMapper>
#include <QDir>
#include <QPushButton>
#include <QMenu>
#include <QMap>
#include "ui_algtest.h"
#include "qcustomplot.h"
#include <QtAlgorithms>
//Ìí¼Ó opencv
#include <opencv2/opencv.hpp>
#include <opencv2\highgui\highgui.hpp>
#include <opencv2\core\operations.hpp>
using namespace cv;

class algtest : public QMainWindow {
    Q_OBJECT

public:
    algtest ( QWidget *parent = 0 );
    ~algtest();

private:
    Ui::algtestClass ui;
private:
    QSignalMapper * m_signalMapper_basic;
    QDir * m_imageDir_basic;
    QMenu * m_p_MouseMenu;
    QString m_image_name;
    QString m_image_folder;
    QCustomPlot* m_plot;
private:
    void Mat2QImage ( QImage & qImg, Mat cvImg );
    void display_img ( Mat & img_rgb );
    void draw_line ( QVector<double> & x, QVector<double> & y );
    void OnReflashImages();
    void OnChangeImage ( const QString & key );
private:

    void OnMapperMessages ( const QString &  key );

};

#endif // ALGTEST_H
