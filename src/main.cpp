#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QSslSocket>
#include <QDebug>

#include "vehiclemodel.h"
#include "apiclient.h"

int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
    QGuiApplication app(argc, argv);

    qDebug() << "SSL Support:" << QSslSocket::supportsSsl();
    qDebug() << "SSL Build Version:" << QSslSocket::sslLibraryBuildVersionString();
    qDebug() << "SSL Runtime Version:" << QSslSocket::sslLibraryVersionString();
    app.setOrganizationName("CubaEV");
    app.setApplicationName("CubAutosFinder");
    app.setApplicationVersion("1.0.0");

    VehicleModel vehicleModel;
    ApiClient apiClient;

    QObject::connect(&apiClient, &ApiClient::resultsReceived,
                     &vehicleModel, &VehicleModel::loadFromJson);

    QQmlApplicationEngine engine;
    engine.rootContext()->setContextProperty("vehicleModel", &vehicleModel);
    engine.rootContext()->setContextProperty("apiClient", &apiClient);

    const QUrl url(QStringLiteral("qrc:/qml/main.qml"));
    engine.load(url);

    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}
